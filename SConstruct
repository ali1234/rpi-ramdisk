import pathlib
from textwrap import TextWrapper

import sh

env = Environment(tools=[])
env.Tool('textfile')


class Functions(object):

    @staticmethod
    def repo_scan(*args):
        for dir in args:
            p = pathlib.Path(str(dir.abspath))
            yield from (str(p / f) for f in sh.git('-C', str(p), 'ls-files', '-mo', '--exclude-standard').split('\n')[:-1])
            yield sh.git('-C', str(p), 'rev-parse', '--absolute-git-dir').split('\n')[0] + '/logs/HEAD'

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

tftp_root = Value('tftp-root={:s}'.format(boot.abspath))
env.Substfile('dnsmasq.conf', ['dnsmasq.conf.in', tftp_root, Value('')])

