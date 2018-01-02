from mkv import Mkv
from mkv import LISTS_TYPES

__author__ = 'nekmo'


class MkvSource(Mkv):
    _no_videos = '-D'
    _no_audios = '-A'
    _no_subtitles = '-S'
    _no_tags = '-T'
    _no_global_tags = '--no-global-tags'
    _tracks_types_args = {
        'videos': 'video-tracks', 'audios': 'audio-tracks', 'subtitles': 'subtitle-tracks',
        'tags': 'tracks-tags', 'global_tags': 'global-tags',
    }

    types = ['videos', 'audios', 'subtitles', 'tags', 'global_tags']

    def __init__(self, files):
        self._copy_videos = [self._no_videos]
        self._copy_audios = [self._no_audios]
        self._copy_subtitles = [self._no_subtitles]
        self._copy_tags = [self._no_tags]
        self._copy_global_tags = [self._no_global_tags]

        super(MkvSource, self).__init__()
        if not isinstance(files, LISTS_TYPES):
            files = [files]
        self.files = files

    def _set_type_elements(self, type, elements):
        var_name = '_copy_%s' % type
        if elements  and elements[0] == 'all':
            elements = True
        elif not elements or elements[0] is False:
            elements = [getattr(self, '_no_%s' % type)]
        else:
            elements = self._normatize_input_options(elements)
            elements = self._argument_value(self._tracks_types_args[type], elements)
        setattr(self, var_name, elements)

    def copy_videos(self, *elements):
        self._set_type_elements('videos', elements)

    def copy_audios(self, *elements):
        self._set_type_elements('audios', elements)

    def copy_subtitles(self, *elements):
        self._set_type_elements('subtitles', elements)

    def copy_tags(self, *elements):
        self._set_type_elements('track_tags', elements)

    def copy_global_tags(self, *elements):
        self._set_type_elements('global-tags', elements)

    def get_args(self):
        for type in self.types:
            value = getattr(self, '_copy_%s' % type)
            if value is True: continue
            self.arguments.extend(value)
        return self.arguments