# Set environment variables *before* importing libraries that use them
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow INFO/WARNING/ERROR messages (actually, delete TF entirely in this env)
os.environ['LOGLEVEL'] = 'ERROR'         # Suppress general Python logging below ERROR

# Suppress Python warnings
import warnings
warnings.filterwarnings('ignore', category=FutureWarning) # Ignore future warnings (like max_new_tokens)
warnings.filterwarnings('ignore', message=".*Trying to infer the `batch_size` from the input.*")
warnings.filterwarnings('ignore', message=".*The attention mask is not set.*")
warnings.filterwarnings('ignore', message=".*You are attempting to use Flash Attention 2.0.*")
# Add more specific message filters here if other warnings appear

import torch
import subprocess
import glob
import textwrap
import sys
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
# Set logging level for transformers specifically *after* import if needed
from transformers import logging as hf_logging
hf_logging.set_verbosity_error() # Only show errors from transformers

# --- Configuration ---
# Use GPU if available, otherwise CPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Model ID for Distil-Whisper
model_id = "distil-whisper/distil-large-v3"
# Supported audio file extensions
audio_extensions = ["*.m4a", "*.mp3", "*.m2a", "*.ogg", "*.wav"]
# --- End Configuration ---

# --- Helper Function to get script's directory ---
def get_script_directory():
    """Gets the directory where the script is located."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path

# --- Model Loading ---
# print(f"Loading model: {model_id}...") # SILENCED
try:
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
        attn_implementation="flash_attention_2" if torch.cuda.is_available() and torch_dtype == torch.float16 else "sdpa"
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)

    # Create the transcription pipeline
    # CORRECTED: Removed the duplicate max_new_tokens argument
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        # max_new_tokens=128, # <-- REMOVED THIS DIRECT ARGUMENT
        chunk_length_s=15,
        batch_size=16, # Keep your working batch size
        torch_dtype=torch_dtype,
        device=device,
        # Keep this version inside generate_kwargs as recommended by the warning
        generate_kwargs={"max_new_tokens": 128}
    )

except Exception as e:
    print(f"FATAL: Error loading model or creating pipeline: {e}", file=sys.stderr) # Print fatal errors to stderr
    exit(1)


# --- File Discovery ---
script_dir = get_script_directory()

files_to_process = []
for ext in audio_extensions:
    files_to_process.extend(glob.glob(os.path.join(script_dir, ext)))

if not files_to_process:
    print("No audio files found in the script's directory.", file=sys.stderr) # Print error to stderr
    exit(0)

# Text wrapper for cleaner console output (still needed for the transcription itself)
wrapper = textwrap.TextWrapper(width=80,
    initial_indent="", # No indent for pure transcription output
    subsequent_indent="", # No indent
    break_long_words=False,
    break_on_hyphens=False)

# --- Processing Loop ---
for audio_path in files_to_process:
    base_filename = os.path.basename(audio_path)
    filename_no_ext = os.path.splitext(base_filename)[0]
    current_file_path = audio_path

    # --- (Optional) Rename file if it contains spaces ---
    if ' ' in base_filename:
        # print(f"  WARNING: '{base_filename}' contains spaces.") # SILENCED
        new_base_filename = base_filename.replace(' ', '-')
        new_file_path = os.path.join(script_dir, new_base_filename)
        try:
            os.rename(audio_path, new_file_path)
            # print(f"  Renamed to: '{new_base_filename}'") # SILENCED
            current_file_path = new_file_path
            filename_no_ext = os.path.splitext(new_base_filename)[0]
        except OSError as e:
            print(f"Error renaming file '{base_filename}': {e}. Skipping.", file=sys.stderr) # Print error to stderr
            continue

    # --- Define temporary WAV file path ---
    temp_wav_path = os.path.join(script_dir, f"{filename_no_ext}_TEMP_16k.wav")
    transcript_path = os.path.join(script_dir, f"{filename_no_ext}.md")

    # --- Convert audio to 16-bit WAV format required by Whisper ---
    try:
        ffmpeg_command = [
            'ffmpeg',
            '-y',
            '-i', current_file_path,
            '-ar', '16000',
            '-ac', '1',
            '-c:a', 'pcm_s16le',
            temp_wav_path
        ]
        # Use subprocess.DEVNULL to hide ffmpeg's own output
        process = subprocess.run(ffmpeg_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except FileNotFoundError:
        print("Error: ffmpeg command not found. Please ensure ffmpeg is installed and in your system's PATH.", file=sys.stderr)
        continue
    except subprocess.CalledProcessError as e:
        # Try running again *without* hiding stderr to capture the actual ffmpeg error
        try:
            process = subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e_inner:
             print(f"Audio conversion failed for '{base_filename}' with error code {e_inner.returncode}.", file=sys.stderr)
             print(f"FFmpeg command: {' '.join(ffmpeg_command)}", file=sys.stderr)
             print(f"FFmpeg stderr:\n{e_inner.stderr}", file=sys.stderr)
        # Clean up potentially incomplete temp file
        if os.path.exists(temp_wav_path):
            try: os.remove(temp_wav_path)
            except OSError: pass
        continue
    except Exception as e:
        print(f"An unexpected error occurred during conversion for '{base_filename}': {e}", file=sys.stderr)
        continue


    # --- Transcribe the temporary WAV file ---
    transcription = "" # Initialize transcription text
    try:
        if not os.path.exists(temp_wav_path):
             print(f"Error: Temporary WAV file '{temp_wav_path}' not found after conversion attempt for '{base_filename}'.", file=sys.stderr)
             continue

        result = pipe(temp_wav_path)
        transcription = result["text"].strip()

        # --- Output ONLY the Transcription ---
        if transcription:
             print(wrapper.fill(transcription)) # <<< ONLY DESIRED OUTPUT

        # --- Save Transcript to .md file ---
        try:
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(transcription)
                print(f"  Transcript saved to: {os.path.basename(transcript_path)}")
        except IOError as e:
            print(f"Error saving transcript file for '{base_filename}': {e}", file=sys.stderr)

    except Exception as e:
        print(f"Transcription failed for '{base_filename}': {e}", file=sys.stderr)
        if "out of memory" in str(e).lower():
            print("  Consider reducing batch_size or using a smaller model.", file=sys.stderr)

    # --- Cleanup: Delete the temporary WAV file ---
    finally:
        if os.path.exists(temp_wav_path):
            try:
                os.remove(temp_wav_path)
            except OSError as e:
                pass # Silently ignore cleanup error if needed

# create a directory for all your audio files and put this python script in it
# "uv run whisper_run.py"
