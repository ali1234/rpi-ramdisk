import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {

    'requires': [],

    'sysroot_debs': [
        # core dependencies
        'libglib2.0-dev', 'libreadline-dev', 'libssl1.0-dev', 'zlib1g-dev', 'libasound2-dev',
        'libgirepository1.0-dev', 'uuid-dev', 'libsoup2.4-dev',
        'libxml2-dev', 'libgee-0.8-dev', 'libsqlite3-dev', 'valac', 'liborc-0.4-dev', 'liborc-0.4-dev-bin',
        'libraspberrypi-dev',
        # libav
        #'libavcodec57', 'libavfilter6', 'libavformat57', 'libavutil55', 'libavdevice57',
    ],

    'root_debs': [
        'liborc-0.4-0', 'libasound2', 'libxml2', 'libsoup2.4-1', 'libraspberrypi0',
        # libav
        #'libavcodec-dev', 'libavfilter-dev', 'libavformat-dev', 'libavutil-dev',
    ],

    'target': this_dir / 'gstreamer.tar.gz',
    'install': [],

}

from ... import sysroot, jobs

env = sysroot.env.copy()


prefix = '/opt/gstreamer'
stage = this_dir / 'stage'


# tell g-ir-scanner about the sysroot.
env['CFLAGS'] = f'--sysroot={sysroot.sysroot} {sysroot.arch_cflags}'

env['LDFLAGS'] = ' '.join([
    f'--sysroot={sysroot.sysroot}',
    f'-L{sysroot.sysroot}/opt/vc/lib',
    # for rpi-camsrc:
    f'-Wl,--rpath-link,{sysroot.sysroot}/opt/vc/lib',
    f'-L{stage}/opt/gstreamer/lib',
])

env['CPPFLAGS'] = ' '.join([
    f'--sysroot={sysroot.sysroot}',
    # put dispmanx/EGL flags into the global state. https://bugzilla.gnome.org/show_bug.cgi?id=770987
    f'-I{sysroot.sysroot}/opt/vc/include',
    f'-I{sysroot.sysroot}/opt/vc/include/interface/vcos/pthreads',
    f'-I{sysroot.sysroot}/opt/vc/include/interface/vmcs_host/linux',
    f'-I{stage}/opt/gstreamer/include/gstreamer-1.0',
])


# add stage to the paths. every package which uses this env should do this (ie rygel).
env['PKG_CONFIG_LIBDIR'] += ':' + str(stage / prefix[1:] / 'lib/pkgconfig')
env['XDG_DATA_DIRS'] += ':' + str(stage / prefix[1:] / 'share')

repos = [this_dir / d for d in [
    'gstreamer', 'gst-plugins-base', 'gst-plugins-good', 'gst-plugins-bad', 'gst-plugins-ugly',
    'gst-libav', 'gst-omx', 'gst-rtsp-server', 'gst-rpicamsrc',
]]

CROSS_OPTS = ' '.join([
    '--host=arm-linux-gnueabihf',
    '--build=x86_64-linux-gnu',
    f'--prefix={prefix}',
    f'--with-sysroot={sysroot.sysroot}',
    f'--with-libgcrypt-prefix={sysroot.sysroot}/usr'
])

COMMON_OPTS = ' '.join([
    '--disable-dependency-tracking', '--disable-maintainer-mode', '--disable-fatal-warnings',
    '--disable-debug', '--disable-docbook', '--disable-gtk-doc', '--disable-gtk-doc-html',
    '--disable-gtk-doc-pdf', '--disable-examples', '--disable-benchmarks',
    '--enable-introspection=yes',
])

NODEBUG_OPTS = ' '.join([
    '--enable-gobject-cast-checks=no', '--enable-glib-asserts=no', '--disable-gst-debug',
    '--disable-gst-tracer-hooks', '--disable-trace', '--disable-alloc-trace', '--disable-valgrind',
])

PLUGIN_OPTS = ' '.join([
    '--enable-orc', '--disable-x', '--disable-xvideo', '--disable-xshm', '--disable-wayland',
    '--disable-fbdev', '--disable-jack', '--disable-pulse', '--disable-cairo',
    '--disable-gdk_pixbuf', '--disable-festival', '--disable-flite', '--disable-fluidsynth',
])

DISPMANX_OPTS = ' '.join([
    '--disable-opengl', '--enable-gles2', '--enable-egl', '--disable-glx', '--enable-dispmanx',
    '--with-gles2-module-name=/opt/vc/lib/libbrcmGLESv2.so', '--with-egl-module-name=/opt/vc/lib/libbrcmEGL.so',
])

OMX_OPTS = ' '.join([
    '--with-omx-target=rpi',
    f'--with-omx-header-path={sysroot.sysroot}/opt/vc/include/IL',
])

RPICAMSRC_OPTS = ' '.join([
    f'--with-rpi-header-dir={sysroot.sysroot}/opt/vc/include',
])

def build_repo(repo, extra_opts=''):
    call([
        f'cd {repo} && ./autogen.sh {CROSS_OPTS} {COMMON_OPTS} {NODEBUG_OPTS} {extra_opts}',

        # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=297726
        # reverse debian-specific change in libtool that breaks cross compiling
        f'cd {repo} && sed -i -e "s/^link_all_deplibs=no$/link_all_deplibs=unknown/" libtool',

        f'make -j{jobs} -C {repo}',
        f'make -j{jobs} -C {repo} DESTDIR={stage} install-strip',
    ], env=env, shell=True)


@command(produces=[package['target']], consumes=[sysroot.sysroot, sysroot.toolchain])
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
        # libtool sucks donkey balls
        f'mkdir -p {sysroot.sysroot}/opt',
        f'ln -sf {stage}{prefix} {sysroot.sysroot}{prefix}',
    ])

    build_repo(repos[1], f'{PLUGIN_OPTS} {DISPMANX_OPTS}') # base
    build_repo(repos[2], f'{PLUGIN_OPTS}') # good
    build_repo(repos[3], f'{PLUGIN_OPTS} --disable-gl') # bad
    build_repo(repos[4], f'{PLUGIN_OPTS}') # ugly
    #build_repo(repos[5], f'{PLUGIN_OPTS}') # libav
    build_repo(repos[6], f'{PLUGIN_OPTS} {OMX_OPTS}') # omx
    build_repo(repos[7]) # rtsp

    # rpicamsrc
    call([
        f'cd {repos[8]} && autoreconf --verbose --force --install && ./configure {CROSS_OPTS} {RPICAMSRC_OPTS} {COMMON_OPTS} {NODEBUG_OPTS}',
        f'make -j{jobs} -C {repos[8]}',
        f'make -j{jobs} -C {repos[8]} DESTDIR={stage} install-strip',
    ], env=env, shell=True)

    call([
        f'mkdir -p {stage}/etc/ld.so.conf.d',
        f'echo {prefix}/lib > {stage}/etc/ld.so.conf.d/opt-gstreamer.conf',

        f'tar -C {stage} --exclude=.{prefix}/doc --exclude=.{prefix}/include \
            --exclude=*.la --exclude=.{prefix}/share/locale --exclude=.{prefix}/share/aclocal \
            --exclude=.{prefix}/share/bash-completion \
            -czf {package["target"]} .'

    ], shell=True)


@command()
def clean():
    call([f'git -C {repo} clean -dfxq' for repo in repos])
    call([f'rm -rf --one-file-system {stage} {package["target"]}'])
