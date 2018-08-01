import pathlib
import subprocess
from textwrap import TextWrapper

import sh

env = Environment(tools=[])
env.Tool('textfile')


AddOption('--verbose', dest='verbose', action='store_true',  help='Output verbose build logs.')


env['REDIRECT'] = '' if GetOption('verbose') else ' > /dev/null'

env['MAKE'] = 'make -j8'

class Functions(object):

    @staticmethod
    def repo_scan(*args):
        for dir in args:
            p = pathlib.Path(str(dir.abspath))
            yield from (str(p / f) for f in sh.git('-C', str(p), 'ls-files', '-mo', '--exclude-standard').split('\n')[:-1])
            yield sh.git('-C', str(p), 'rev-parse', '--absolute-git-dir').split('\n')[0] + '/logs/HEAD'

    @staticmethod
    def dir_scan(dir):
        # stable recursive checksum of directory
        return subprocess.check_output([
            'sh', '-c',
            f'cd {dir.abspath} && find -type f -exec sha256sum {{}} \; | sort | sha256sum'
        ])

    @staticmethod
    def textwrap(string_or_list, prefix='', join=' ', width=120):
        """Generates wordwrapped lines for config files."""
        wrapper = TextWrapper(
            break_long_words=False, break_on_hyphens=False,
            initial_indent=prefix, subsequent_indent=prefix,
            width=width,
        )

        if isinstance(string_or_list, str):
            return wrapper.fill(string_or_list)
        else:
            return wrapper.fill(join.join(string_or_list))


env['FUNCTIONS'] = Functions


def print_cmd_line(message, targets, sources, env):
    print('\033[33m\033[1m', targets[0], ': \033[39m', message, '\033[0m', sep='')

env['PRINT_CMD_LINE_FUNC'] = print_cmd_line

SConscript([
    'kernel/SConscript',
    'firmware/SConscript',
    'raspbian/SConscript',
], 'env')

boot = Dir('boot/')

boot_build = env.Command('boot.zip', ['raspbian/initrd', 'firmware/firmware.tar.gz', 'kernel/kernel-boot.tar.gz', 'kernel/kernel7-boot.tar.gz'], [

    'mkdir -p ${STAGE}',
    'rm -rf --one-file-system ${STAGE}/*',
    'cp ${SOURCES[0]} ${STAGE}',
    'for tb in ${SOURCES[1:]}; do tar -xf $$tb -C ${STAGE}; done',
    'cd ${STAGE} && zip -qr ${TARGET.abspath} *',

], STAGE=boot)
env.Clean(boot_build, boot)

env.Substfile('dnsmasq.conf', 'dnsmasq.conf.in', SUBST_DICT={'@TFTP_ROOT@': boot.abspath})

