# subtitle-adder
A Python script for adding subtitles to all episodes in a season. The script can handle all file formats that [MKVtoolNix](https://mkvtoolnix.download/downloads.html) supports. The scripts saves all files in the mkv format.
## Requirements
Python 3+

Mkvmerge from MKVtoolNix which can be downloaded [here]((https://mkvtoolnix.download/downloads.html). If you are using a portable version you must use the ```-p``` flag to point to the folder where the mkvmerge file is located.
## Installation
Clone the repository using
```git
git clone https://github.com/Birath/subtitle-adder.git
```
or [download](https://github.com/Birath/subtitle-adder/archive/master.zip) it manually.
## Usage
Place the video files from the season that you want to add subtitle to in one folder and your subtitle files in **another** folder. Make sure that all files are in the correct order when sorting alphabetically. Then run
```
python subtitle_adder.py /path/to/video-files /path/to/subtitle-files language-code name
```
If you want to set the output folder use the ```-of``` flag like this
```
python subtitle_adder.py /path/to/video-files /path/to/subtitle-files language-code name -of /path/to/output
```
To change the name of the output files, use the ```-o``` flag. Use \*NUM* in place of the episode number when typing the name. Example:
```
python subtitle_adder.py video-files subtitle-files lang name -o "Game Of Thrones S01E*NUM*"
```

The full list of flags can be seen by running
```
python subtitle_adder.py -h
```
Which shows the following

```
usage: subtitle_adder.py [-h] [-o FILE] [-of FOLDER] [-d True/False]
                         [-f True/False] [-p PATH] [-ri True/False]
                         ep-folder sub-folder LANG NAME

Add subtitles to all episodes in a season

positional arguments:
  ep-folder             The folder where the video files are located
  sub-folder            The folder where the subtitle files are located
  LANG                  The language code (e.g., eng, swe) of the subtitles
  NAME                  The name of the subtitle track

optional arguments:
  -h, --help            show this help message and exit
  -o, --output FILE     The file names of the outputs (default: Same as
                        input). Use *NUM* to insert the episode number in the
                        name (ex: Game Of Thrones S01E*NUM*)
  -of, --output-folder FOLDER
                        The folder where the output is saved (default: Same as
                        script)
  -d, --default True/False
                        If the subtitles should be default or not (default:
                        True)
  -f, --forced True/False
                        If the subtitles should be forced or not (default:
                        False)
  -p, --path PATH       The path to mkvmerge (default: same directory as the
                        script)
  -ri, --remove-input True/False
                        Removes all input files. This can not be reversed
                        (default: False)
```
## Example
```
python subtitle_adder.py "\Videos\Game Of Thrones S01" "\Videos\Game of Thrones S01 Subs" swe Swedish -p Programs\mkvtoolnix -of "\Videos\Game Of Thrones S01 Subbed" -o "Game of Thrones S01E*NUM*"
```
This will add Swedish subtitles to all episodes in the first season of Game Of Thrones and save them to the *Game of Thrones S01 Subbed* folder. It also points to location where the mkvmerge is located *(Programs\mkvtoolnix)* using the ```-p``` flag.  
## Credits
The [python-mkv](https://pypi.python.org/pypi/mkv/0.1.5) module is created by Nekmo. I've done some minor changes to it to support newer python versions, so the script is not compatible with the PyPi package.
