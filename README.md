![Designer (2)](https://github.com/frasertajima/whisper_bulk_transcription/assets/69366820/8af38525-f365-416f-9460-f7734cd5a7b0)

# whisper_bulk_transcription
## Bulk transcription of audio files to text using OpenAI Whisper (https://github.com/openai/whisper)

`whisper-distil-CUDA` builds upon whisper, is easier to setup in Fedora Silverblue and uses CUDA for astonishing speed (https://huggingface.co/distil-whisper/distil-large-v2). Accuracy is almost as good as the CPU bound `whisper to text` model which requires a bit more setup (https://github.com/ggerganov/whisper.cpp). The directory versions of these two ASR handle bulk transcription. 

## keep a separate copy of your audio files:
Note that audio files with spaces will be renamed: "Track 13.wav" will be renamed "Track-13.wav" in order to enable ffmpeg to injest the file correctly (otherwise ffmpeg will complain it cannot find the "Track" file as it cuts off the name after the space. **Renaming the file has the effect of resetting the file date to today so make sure you have a backup if the original file metadata is important.**

https://felixquinihildebet.wordpress.com/2024/03/16/distil-whisper-is-the-tipping-point/




## colab version is archived
The original Colab notebook is left in for reference. Local processing ensures greater confidentiality and security and is always accessible.

Runs in Google Colab with GPU support. Can be modified to run locally as a Jupyter notebook (by changing `filename` to a local directory such as "/mnt/d/voice memos/"). 

Google Colab runs out of memory and crashes with the `model` set to large (but it will run the large model with enough RAM locally).

https://felixquinihildebet.wordpress.com/2022/10/03/how-to-transcribe-hundreds-of-audio-files-into-text-using-openai-whisper/
