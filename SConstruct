import pathlib

import sh

env = Environment()
env.Tool('textfile')


class Functions(object):

    @staticmethod
    def repo_scan(dir):
        p = pathlib.Path(str(dir.abspath))
        yield from (str(p / f) for f in sh.git('-C', str(p), 'ls-files', '-mo', '--exclude-standard').split('\n')[:-1])
        yield sh.git('-C', str(p), 'rev-parse', '--absolute-git-dir').split('\n')[0] + '/logs/HEAD'


env['FUNCTIONS'] = Functions()


SConscript([
    'kernel/SConscript',
    'firmware/SConscript',
    'packages/SConscript',
], 'env')

boot_dir = Dir('boot/')
tftp_root = Value('tftp-root={:s}'.format(boot_dir.abspath))

env.Substfile('dnsmasq.conf', ['dnsmasq.conf.in', tftp_root, Value('')])

