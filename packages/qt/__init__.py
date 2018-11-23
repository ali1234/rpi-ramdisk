import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {

    'requires': [],

    'sysroot_debs': [
        'libfontconfig1-dev', 'libmtdev-dev', 'libudev-dev', 'libts-dev', 'flex', 'freetds-dev',
        'libasound2-dev', 'libaudio-dev', 'libdbus-1-dev', 'libfreetype6-dev', 'libglib2.0-dev',
        'libjpeg-dev', 'libmng-dev', 'libpam0g-dev', 'libpng-dev', 'libreadline-dev', 'libssl1.0-dev',
        'libtiff-dev', 'zlib1g-dev', 'libjpeg-dev', 'libraspberrypi-dev',
    ],

    'root_debs': [
        'libraspberrypi0', 'libpng12-0', 'libglib2.0-0', 'libmtdev1', 'libts-0.0-0', 'libfontconfig1',
        'libfreetype6', 'libssl1.0.2', 'libjpeg62-turbo',
    ],

    'target': this_dir / 'qt.tar.gz',
    'install': [],

}

from ... import sysroot

env = sysroot.env.copy()


prefix = '/opt/qt'
qt_host = this_dir / 'qt-host'
qmake = qt_host / 'bin' / 'qmake'
stage = this_dir / 'stage'

repos = [this_dir / r for r in ['qtbase', 'qtxmlpatterns', 'qtdeclarative']]


@command(produces=[package['target'], qmake], consumes=[sysroot.sysroot, sysroot.toolchain])
def build():

    call([f'git -C {repo} clean -dfxq' for repo in repos])
    
    call([
        f'rm -rf --one-file-system {stage} {qt_host}',

        f'cd {repos[0]} && ./configure -release -opengl es2 -device linux-rasp-pi2-g++ \
            -qpa eglfs -no-libinput -no-linuxfb -no-xcb -no-kms -no-gbm \
            -no-gtk -no-widgets -no-compile-examples -no-sql-tds \
            -device-option CROSS_COMPILE={sysroot.cross_compile} -sysroot {sysroot.sysroot} \
            -opensource -confirm-license -make libs -strip -optimize-size \
            -prefix {prefix} -extprefix {stage}/{prefix} -hostprefix {qt_host}',
    
        f'make -j8 -C {repos[0]}',
        f'make -j8 -C {repos[0]} install',
    ], env=env, shell=True)

    for repo in repos[1:]:
        call([
            f'cd {repo} && {qmake}',
            f'make -j8 -C {repo}',
            f'make -j8 -C {repo} install',
        ], env=env, shell=True)

    call([
        f'mkdir -p {stage}/etc/ld.so.conf.d',
        f'echo {prefix}/lib > {stage}/etc/ld.so.conf.d/opt-qt.conf',
    
        f'tar -C {stage} --exclude=.{prefix}/doc --exclude=.{prefix}/include \
            --exclude=.{prefix}/lib/cmake --exclude=.{prefix}/lib/pkgconfig \
            -czf {package["target"]} .'
    
    ], env=env)


@command()
def clean():
    call([f'git -C {repo} clean -dfxq' for repo in repos])
    call([f'rm -rf --one-file-system {stage} {package["target"]}'])
