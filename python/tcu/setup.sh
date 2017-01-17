#!/bin/bash

# check if user is root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

TARGET_DIR="/opt/tcu"
SYSTEMD_DIR="/etc/systemd/system"

# get the source directory
SOURCE_DIR="$(dirname $0)"

install() {
    echo "installing TCU to [ $TARGET_DIR ]..."

    # make the target directory
    if [ ! -d "$TARGET_DIR" ]; then
      mkdir -p ${TARGET_DIR}
    fi

    # copy files
    cp -r ${SOURCE_DIR}/* ${TARGET_DIR}

    # set permissions
    chmod u+x ${TARGET_DIR}/tcu.py

    # installing service file
    if [ ! -e "$SYSTEMD_DIR/tcu.service" ]; then
        ln -s ${TARGET_DIR}/systemd/tcu.service ${SYSTEMD_DIR}
    fi

    # reload systemd
    systemctl daemon-reload

    # display status
    systemctl status tcu.service
}

remove() {
    echo "removing TCU..."

    # stop the service
    systemctl stop tcu.service

    # remove the service file
    if [ -e "$SYSTEMD_DIR/tcu.service" ]; then
        rm ${SYSTEMD_DIR}/tcu.service
    fi

    # remove the install directory
    if [ -d "$TARGET_DIR" ]; then
        rm -rf ${TARGET_DIR}
    fi

    # reload systemd
    systemctl daemon-reload
}

case "$1" in
  install)
    install
    ;;
  remove)
    remove
    ;;
  *)
    echo "unknown setup command [ $1 ], please use [ install|remove ]."
	exit 1
	;;
esac

echo "good bye"
exit 0