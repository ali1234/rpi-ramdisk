import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {

    'requires': ['gstreamer'],

    'sysroot_debs': ['libmediaart-2.0-dev'],

    'root_debs': [
        'libgee-0.8-2', 'libtiff5', 'libgdk-pixbuf2.0-0', 'libmediaart-2.0-0',
    ],

    'target': this_dir / 'rygel.tar.gz',
    'install': [],

}

from ... import sysroot
from .. import gstreamer

env = gstreamer.env.copy()


prefix = '/opt/rygel'
stage = this_dir / 'stage'


# add stage to the paths. every package which uses this env should do this (ie rygel).
env['PKG_CONFIG_LIBDIR'] += ':' + str(stage / prefix[1:] / 'lib/pkgconfig')
env['XDG_DATA_DIRS'] += ':' + str(stage / prefix[1:] / 'share')


repos = [this_dir / d for d in [
    'gssdp', 'gupnp', 'gupnp-av', 'gupnp-dlna', 'gupnp-tools', 'rygel',
]]


CROSS_OPTS = ' '.join([
    '--host=arm-linux-gnueabihf',
    '--build=x86_64-linux-gnu',
    f'--prefix={prefix}',
    f'--with-sysroot={sysroot.sysroot}',
    f'--with-libgcrypt-prefix={sysroot.sysroot}/usr'
])


RYGEL_OPTS = ' '.join([
    '--without-ui', '--disable-media-export-plugin', '--disable-tracker-plugin',
    '--disable-external-plugin', '--disable-ruih-plugin', '--disable-mpris-plugin', '--enable-apidocs=no',
])


def build_repo(repo, extra_opts):
    call([
        f'cd {repo} && ./autogen.sh {CROSS_OPTS} {gstreamer.COMMON_OPTS} {gstreamer.NODEBUG_OPTS} {extra_opts}',
        f'make -j8 -C {repo}',
        # gupnp-dlna parallel install fails
        # see https://bugzilla.gnome.org/show_bug.cgi?id=720053
        f'make -C {repo} DESTDIR={stage} install-strip',
    ], env=env, shell=True)


@command(produces=[package['target']], consumes=[gstreamer.package['target']])
def build():

    for repo in repos:
        call([
            f'git -C {repo} clean -dfxq',
        ])

    call([
        f'rm -rf --one-file-system {stage}',

        f'mkdir -p {stage}{prefix}/lib',
        f'mkdir -p {stage}{prefix}/include/gstreamer-1.0',
    ])

    build_repo(repos[0], '')

    call([
        f'mkdir -p {sysroot.sysroot}/opt',
        f'ln -sf {stage}{prefix} {sysroot.sysroot}{prefix}',
    ])

    for r in repos[1:-2]:
        build_repo(r, '')

    build_repo(repos[-1], RYGEL_OPTS)

    call([
        f'mkdir -p {stage}/etc/ld.so.conf.d',
        f'echo {prefix}/lib > {stage}/etc/ld.so.conf.d/opt-gstreamer.conf',

        f'tar -C {stage} --exclude=.{prefix}/doc --exclude=.{prefix}/include \
            --exclude=.{prefix}/lib/pkgconfig --exclude=.{prefix}/share/man \
            --exclude=*.la --exclude=.{prefix}/share/locale --exclude=.{prefix}/share/aclocal \
            --exclude=.{prefix}/share/bash-completion \
            -czf {package["target"]} .'

    ], shell=True)
