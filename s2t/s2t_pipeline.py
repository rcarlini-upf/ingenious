import os
import tempfile
import subprocess

from sox import file_info


class S2TPipeline:

    list_file_format = "{id}\t{path}\t{duration}\t{transcript}\n"

    def __init__(self, base_cfg_path='ASR/conf/decode_partial.cfg'):

        with open(base_cfg_path) as base_cfg:
            self.cfg_base = base_cfg.read()

    def _call_process(self, lst_path, outdir_path):

        with tempfile.NamedTemporaryFile() as cfg_fd:

            cfg_fd.write(self.cfg_base)
            cfg_fd.write('--test={0}\n'.format(lst_path))
            cfg_fd.write('--sclite={0}\n'.format(outdir_path))

            arg_list = ['root/wav2letter/build/Decoder', '--flagsfile', cfg_fd.name]
            subprocess.run(args=arg_list)

    def process(self, audio_path):

        duration = file_info.duration(audio_path)

        list_dict = {
            'id': '000000000',
            'path': audio_path,
            'duration': str(duration),
            'transcript': '<no_transcript>'
        }
        list_data = self.list_file_format.format(**list_dict)

        with tempfile.NamedTemporaryFile() as lst_fd, \
                tempfile.TemporaryDirectory() as outdir_fd:

            lst_fd.write(list_data)

            self._call_process(lst_fd.name, outdir_fd.name)

            output_hyp_filename = 'data#{0}.hyp'.format(lst_fd.name)
            output_hyp_path = os.path.join(outdir_fd, output_hyp_filename)

            with open(output_hyp_path) as fd_output:
                line = fd_output.readline()
                hypothesis, _ = line.split('(', 1)

        return hypothesis
