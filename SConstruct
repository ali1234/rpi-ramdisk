import pathlib
import textwrap

import sh

env = Environment(tools=[])
env.Tool('textfile')

class Functions(object):

    def __init__(self):
        self._wrapper = textwrap.TextWrapper(
            break_long_words=False, break_on_hyphens=False,
            initial_indent='packages=', subsequent_indent='packages=',
            width=120,
        )

    def multistrap_packages(self, *args, **kwargs):
        return self._wrapper.fill(*args, **kwargs)

    def repo_scan(self, *args):
        for dir in args:
            p = pathlib.Path(str(dir.abspath))
            yield from (str(p / f) for f in sh.git('-C', str(p), 'ls-files', '-mo', '--exclude-standard').split('\n')[:-1])
            yield sh.git('-C', str(p), 'rev-parse', '--absolute-git-dir').split('\n')[0] + '/logs/HEAD'


env['FUNCTIONS'] = Functions()

SConscript([
    'kernel/SConscript',
    'firmware/SConscript',
    'raspbian/SConscript',
], 'env')

boot_dir = Dir('boot/')

env.Command(boot_dir, ['raspbian/initrd', 'firmware/firmware.tar.gz', 'kernel/kernel-boot.tar.gz', 'kernel/kernel7-boot.tar.gz'], [
    'rm -rf --one-file-system ${TARGET}',
    'mkdir ${TARGET}',
    'cp ${SOURCES[0]} ${TARGET}',
    'for tb in ${SOURCES[1:]}; do tar -xf $$tb -C ${TARGET}; done',
])

tftp_root = Value('tftp-root={:s}'.format(boot_dir.abspath))
env.Substfile('dnsmasq.conf', ['dnsmasq.conf.in', tftp_root, Value('')])

