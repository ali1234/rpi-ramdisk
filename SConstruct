env = Environment()
env.Tool('textfile')

SConscript([
    'kernel/SConscript',
    'firmware/SConscript',
    'packages/SConscript',
])

boot_dir = Dir('boot/')
tftp_root = Value('tftp-root={:s}'.format(boot_dir.abspath))

env.Substfile('dnsmasq.conf', ['dnsmasq.conf.in', tftp_root, Value('')])

