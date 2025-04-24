![Designer (2)](https://github.com/frasertajima/whisper_bulk_transcription/assets/69366820/8af38525-f365-416f-9460-f7734cd5a7b0)

# whisper_bulk_transcription
Bulk transcription of audio files to text using OpenAI Whisper (https://github.com/openai/whisper)


https://github.com/frasertajima/whisper_bulk_transcription/assets/69366820/28a14703-963d-462e-ac1f-9707e5dff81c



### updated to handle Gnome Podcasts downloaded locally
- added [whisper-youtube](https://github.com/frasertajima/whisper_bulk_transcription/blob/main/whisper-youtube.ipynb) and [whisper-youtube-bulk](https://github.com/frasertajima/whisper_bulk_transcription/blob/main/whisper-youtube-bulk.ipynb) to handle youtube share link and playlist transcriptions, something that might be handly with online courses.
- I finally figured out how to setup whisper.cpp with CUDA in an immutable OS like Fedora Silverblue which cannot install the CUDA toolkit directly [getting blurt to use CUDA in Fedora Silverblue](https://felixquinihildebet.wordpress.com/2024/03/19/getting-blurt-to-use-the-cuda-whisper-cpp-version-in-fedora-silverblue/)
- If you set the `podcasts=True` flag, copies all locally downloaded podcasts to directory specified (best to keep the processing directory clear of old audio files as otherwise bulk transcriptions will only duplicate the work).
- Updated file handling to include `*.m2a` format from Podcasts (https://apps.gnome.org/en-GB/Podcasts/). This may be an efficient way to scan podcasts that have pilled up but which you have not had time to listen to. By converting to text quickly, you can scan to see which podcasts might be of interest (and send the text file to a Kindle). Also handy if you need to copy information contained in the podcast.

- Added a utility to gather up all markdown (`distl-whisper`) or text (`whisper`) files generated in the working directory into a single file for ease of scanning podcast text. The file is stored in the same directory as the Jupyter notebook. Make sure to delete all your old podcasts and other files in your working directory ***before*** running a new bulk transcription run. 

- Added [delete_old_podcasts](https://github.com/frasertajima/whisper_bulk_transcription/blob/main/delete_old_podcasts.ipynb) as a utility to delete old podcasts BEFORE transcription to ensure only new podcasts are transcribed. Gnome `Podcasts` app does not have a delete downloaded podcasts function.


## whisper-distil-CUDA and whisper to text
[whisper-distil-CUDA](https://github.com/frasertajima/whisper_bulk_transcription/blob/main/whisper-distil-CUDA.ipynb) builds upon whisper, is easier to setup in Fedora Silverblue and uses CUDA for astonishing speed (https://huggingface.co/distil-whisper/distil-large-v2). Accuracy is almost as good as the CPU bound [whisper to text](https://github.com/frasertajima/whisper_bulk_transcription/blob/main/whisper%20to%20text.ipynb) model which requires a bit more setup (https://github.com/ggerganov/whisper.cpp). The directory versions of these two ASR handle bulk transcription. 

## keep a separate copy of your audio files:
Note that audio files with spaces will be renamed: "Track 13.wav" will be renamed "Track-13.wav" in order to enable ffmpeg to injest the file correctly (otherwise ffmpeg will complain it cannot find the "Track" file as it cuts off the name after the space. **Renaming the file has the effect of resetting the file date to today so make sure you have a backup if the original file metadata is important.** Files without whitespaces in their names will not be affected.

https://felixquinihildebet.wordpress.com/2024/03/16/distil-whisper-is-the-tipping-point/
https://felixquinihildebet.wordpress.com/2022/10/03/how-to-transcribe-hundreds-of-audio-files-into-text-using-openai-whisper/


## colab version is archived
The original Colab notebook is left in for reference. Local processing ensures greater confidentiality and security and is always accessible.

Runs in Google Colab with GPU support. Can be modified to run locally as a Jupyter notebook (by changing `filename` to a local directory such as "/mnt/d/voice memos/"). 

Google Colab runs out of memory and crashes with the `model` set to large (but it will run the large model with enough RAM locally).


## command line version
![Screenshot From 2025-04-23 19-13-05](https://github.com/user-attachments/assets/b1032d8c-a2f5-4c53-9137-478880ecf07b)

If you use something like Google Recorder to record your audio, you can download the audio files from the recorder webpage to a dedicated local directory. Save this python script in the same directory and simply run whisper_run.py from the command line. It will then transcribe the audio files and save the text in the same markdown format (without the overhead of loading VSCode and the Jupyter notebooks). This command line workflow of "uv run whisper_run.py" if you have uv installed is much faster when dealing with the many audio files that accumulate over time.




