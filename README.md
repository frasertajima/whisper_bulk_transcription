# whisper_bulk_transcription
## Bulk transcription of audio files to text using OpenAI Whisper (https://github.com/openai/whisper)

Useful when you wish to transcribe hundreds of audio files into text.

Runs in Google Colab with GPU support. Can be modified to run locally as a Jupyter notebook (by changing **filename** to a local directory such as "/mnt/d/voice memos/"). 

Google Colab runs out of memory and crashes with the **model** set to large (but it will run the large model with enough RAM locally).

**Filetype** is restricted to "m4a", "wav", "flac" and "mp3" but this can be expanded to any audio file type supported by Whisper now or in the future. The program will crash if it attempts to transcribe a non-audio file but as directories often have a mix of audio and non-audio files (including hidden files) this filter approach was taken rather than attempting to recover after ingesting a non-audio file (as each transcirption operation takes time).

Read Whisper documentation if you wish to run this locally to install all necessary dependencies. Check to ensure your Colab session is using GPU support (which is considerably faster than running on the CPU). Whisper needs an Nvidia GPU (not AMD GPU) due to Pytorch. Otherwise, it will only run on the CPU (which is much slower).

https://felixquinihildebet.wordpress.com/2022/10/03/how-to-transcribe-hundreds-of-audio-files-into-text-using-openai-whisper/
