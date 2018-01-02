# coding=utf-8
import os
from subprocess import check_call
import mimetypes

from mkv import Mkv, LISTS_TYPES
from mkv.source import MkvSource

mimetypes.init()

mimetypes.add_type('application/x-truetype-font', '.ttf')
mimetypes.add_type('application/vnd.ms-opentype', '.otf')


__author__ = 'nekmo'

"C:\Program Files\MKVToolNix\mkvmerge.exe" \
"--language" "0:jpn" "--track-name" "0:[HDTV] 10bit H.264 - 720p" "--default-track" "0:yes" "--forced-track" "0:no" \
#
"--display-dimensions" "0:1280x720" \
"--language" "1:jpn" "--track-name" "1:AAC 2.0" "--default-track" "1:yes" "--forced-track" "1:no"\
# Audio Tracks --audio-tracks
"-a" "1"\
# Vídeo Tracks --video-tracks
"-d" "0"\
# Vídeo Tracks --subtitle-tracks
"-S" \
# -T, --no-track-tags Don't copy any track specific tags from this file.
"-T" "--no-global-tags" \

"(" "I:\\Fansubbing\\HDTV\\[Canchosos]_Highschool_DxD_BorN_[HDTV]\\01\\[Canchosos]_Highschool_DxD_BorN_-_01_[premux][0917F8FF].mkv" ")" \
#
"--language" "0:spa" "--track-name" "0:Subtítuloa [Latino] - Hagure, Hoshizora & Seigi" "--default-track" "0:yes" "--forced-track" "0:no"\
# -s, --subtitle-tracks
"-s" "0" \
# --no-video
"-D" \
# --no-audio
"-A" \
# Don't copy any track specific tags from this file.
"-T" \
"--no-global-tags" "--no-chapters" "(" "I:\\Fansubbing\\HDTV\\[Canchosos]_Highschool_DxD_BorN_[HDTV]\\01\\[Canchosos] Highschool DxD PorN - 01 [Final].ass" ")"\
#
"--track-order" "0:0,0:1,1:0"\
"--attachment-mime-type" "application/vnd.ms-opentype" "--attachment-name" "BPreplayBold.otf" "--attach-file" \
                                                                                               "I:\\Fansubbing\\HDTV\\[Canchosos]_Highschool_DxD_BorN_[HDTV]\\01\\BPreplayBold.otf"\
# ....
"--title" "[Canchosos] Highschool DxD BorN - 01: ¡Verano en el Inframundo!" \
"--chapter-language" "spa" \
"--chapters" "I:\\Fansubbing\\HDTV\\[Canchosos]_Highschool_DxD_BorN_[HDTV]\\01\\Chapter 01.xml"


class MkvMerge(Mkv):
    command = 'mkvmerge'

    def __init__(self, output):
        super(MkvMerge, self).__init__()
        self.set_arg_value('output', output)

    def add_source(self, source):
        self.arguments.extend(source.get_args())
        self.arguments.extend(['('] + list(source.files) + [')'])

    def add_subtitle(self, file, name, language_code, is_default=None, is_forced=False, order=0):
        # El order siempre es 0 porque el origen es un archivo, con solo 1 track
        self.add_language(language_code, name, is_default, is_forced, order)
        self.set_arg_value('subtitle-tracks', [order, '(', file, ')'])

    def add_chapters(self, file, language_code):
        # El order siempre es 0 porque el origen es un archivo, con solo 1 track
        self.set_arg_value("chapter-language", language_code)
        self.set_arg_value('chapters', file)

    def add_attachments(self, files):
        if not isinstance(files, LISTS_TYPES):
            files = [files]
        for file in files:
            self.set_arg_value('attachment-mime-type', mimetypes.guess_type(file)[0])
            self.set_arg_value('attachment-name', os.path.split(file)[1])
            self.set_arg_value('attach-file', file)

    def add_attachments_from_dir(self, dir):
        for file in os.listdir(dir):
            self.add_attachments(os.path.join(dir, file))

    def set_title(self, name):
        self.set_arg_value('title', name)

    def set_language(self, language_code):
        # DEPRECATED
        self.set_arg_value('chapter-language', language_code)

    def create(self, location=""):
        print(self.arguments)
        check_call([location + self.command] + list(map(str, self.arguments)))


if __name__ == '__main__':

    source = MkvSource('/home/nekmo/Src/Hoshizora/premux/dxd/02/[Canchosos]_Highschool_DxD_BorN_-_02_[premux][AEAF7ED6].mkv')
    source.copy_audios('all')
    source.copy_videos('all')
    mkvmerge = MkvMerge('/tmp/salida.mkv')
    mkvmerge.add_language("jpn", "[HDTV] 10bit H.264 - 720p")
    mkvmerge.add_language("jpn", "AAC 2.0")
    mkvmerge.add_source(source)
    mkvmerge.add_subtitle('/home/nekmo/Src/Hoshizora/premux/dxd/02/[Canchosos] Highschool DxD PorN - 02 [Final].ass',
                          "Subtítulos [Latino] - Hagure, Hoshizora & Seigi", 'spa')
    mkvmerge.add_attachments_from_dir('/home/nekmo/Src/Hoshizora/premux/dxd/02/fonts/')
    mkvmerge.set_title("[Hoshizora] Highschool DxD BorN - 01: ¡Verano en el Inframundo!")
    mkvmerge.set_language('spa')
    mkvmerge.create()
