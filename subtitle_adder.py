from mkv import merge, source
import os
import sys
import argparse
import traceback


def main():
    parser = add_arguments()
    args = parser.parse_args()
    if args.remove_input:
        if not ask_question('This will remove all input files which cannot '
                            'be reversed. Are you sure?'):
            exit(1)

    add_subs_to_season(args.video_input, args.sub_input, args)


def add_arguments():
    """Returns a parser with all arguments"""
    parser = argparse.ArgumentParser(description='Add subtitles to all'
                                                 ' episodes in a season',
                                     formatter_class=CustomFormatter)

    parser.add_argument('video_input',
                        metavar='ep-folder',
                        help='The folder where the video files are located')

    parser.add_argument('sub_input',
                        metavar='sub-folder',
                        help='The folder where the subtitle files are located')

    parser.add_argument('lang',
                        metavar='LANG',
                        help='The language code (e.g., eng, swe) of the'
                             ' subtitles')

    parser.add_argument('name',
                        metavar='NAME',
                        help='The name of the subtitle track')

    parser.add_argument('-o', '--output',
                        metavar='FILE',
                        default=None,
                        help="""The file names of the outputs (default: Same as
                        input). Use *NUM* to insert the episode number in the
                        name (ex: Game Of Thrones S01E*NUM*) """)

    parser.add_argument('-of', '--output-folder',
                        metavar='FOLDER',
                        default="",
                        help='The folder where the output is saved '
                             '(default: Same as script)')

    parser.add_argument('-d', '--default',
                        metavar='True/False',
                        type=str2bool,
                        default=None,
                        choices=[True, False],
                        help='If the subtitles should be default or not '
                             '(default: True)')

    parser.add_argument('-f', '--forced',
                        metavar='True/False',
                        type=str2bool,
                        default=False,
                        choices=[True, False],
                        help='If the subtitles should be forced or not ' 
                             '(default: False)')

    parser.add_argument('-p', '--path',
                        default="",
                        help='The path to  mkvmerge (default: same directory '
                             'as the script)')

    parser.add_argument('-ri', '--remove-input',
                        metavar='True/False',
                        type=str2bool,
                        default=False,
                        choices=[True, False],
                        help='Removes all input files. This can not be '
                             'reversed (default: False)')

    return parser


def str2bool(v):
    """Converts a string to a boolean"""
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def add_subs_to_season(video_folder, sub_folder, args):
    """Adds subtitles to all video files in the video folder"""
    ep_num = 0
    video_files, sub_files = filter_folders(video_folder, sub_folder)
    for video_f, sub_f in zip(video_files, sub_files):
        ep_num += 1

        v_source = get_source(args.video_input, video_f)

        merge_file = create_merge_obj(args.output,
                                      args.output_folder,
                                      video_f,
                                      ep_num)

        merge_file.add_source(v_source)
        merge_file.add_subtitle(os.path.join(args.sub_input, sub_f),
                                args.name,
                                args.lang,
                                is_forced=args.forced,
                                is_default=args.default)
        try:
            merge_file.create(location=os.path.normpath(args.path) + "\\")
            print("Success!")
        except FileNotFoundError as e:
            traceback.print_exc()
            sys.exit("The mkvmerge file could not be found! Try changing its "
                     "path using -p (see -h for more info)")
        if args.remove_input:
            remove_input(sub_folder, sub_f, video_folder, video_f)
            print("Deleted subtitle file {}".format(sub_f))
            print("Deleted video file {}".format(video_f))


def filter_folders(video_files, sub_files):
    """Returns two lists with the files in the two directories"""
    try:
        video_files = [f for f in os.listdir(video_files) if
                       os.path.isfile(os.path.join(video_files, f))]
    except FileNotFoundError:
        traceback.print_exc()
        sys.exit('The folder for the video files could not be found')
    try:
        sub_files = [f for f in os.listdir(sub_files) if
                     os.path.isfile(os.path.join(sub_files, f))]
    except FileNotFoundError:
        traceback.print_exc()
        sys.exit('The folder for the subtitle files could not be found')
    return video_files, sub_files


def get_source(ep_folder, ep_file):
    """Returns a MkvSource object based on the given input"""
    v_source = source.MkvSource(os.path.join(ep_folder, ep_file))
    v_source.copy_audios('all')
    v_source.copy_videos('all')
    return v_source


def create_merge_obj(output, output_folder, ep_file, ep_num):
    """Returns a MkvMerge object based on the given input"""
    if output is None:
        merge_file = merge.MkvMerge(os.path.join(output_folder, ep_file))
    else:
        out_name = output.replace('*NUM*', (str(ep_num) if ep_num >= 10
                                            else "0{}".format(ep_num)))
        merge_file = merge.MkvMerge(os.path.join(output_folder,
                                                 "{}.mkv".format(out_name)))
    return merge_file


def ask_question(question):
    """Asks user a question and returns True if the user answer yes"""
    answer = input("{} (y/n): ".format(question)).lower()
    while answer not in ["y", "yes", "n", "no"]:
        answer = input("Please enter y or n: ")
    return answer in ["y", "yes"]


def remove_input(sub_folder, sub_f, video_folder, video_f):
    """Removes the given subtitle file and video file"""
    os.remove(os.path.join(sub_folder, sub_f))
    os.remove(os.path.join(video_folder, video_f))


class CustomFormatter(argparse.HelpFormatter):
    """Credit to https://stackoverflow.com/a/23941599"""

    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(action.option_strings)

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            # change to
            #    -s, --long ARGS
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    # parts.append('%s %s' % (option_string, args_string))
                    parts.append('{}'.format(option_string))
                parts[-1] += ' {}'.format(args_string)
            return ', '.join(parts)


if __name__ == '__main__':
    main()
