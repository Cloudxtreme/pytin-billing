#!/usr/bin/env bash

if [ -z $1 ];
then
    echo "Where to install?"
    exit 1
fi

if [ -z $2 ];
then
    echo "Specify user?"
    exit 1
fi

SOURCES=$(pwd)
APPROOT=$1
USER=$2

APPNAME=${USER}
APPCONFIG=${SOURCES}/deploy
DJANGOROOT=${APPROOT}/djangoproj

if [ ! -d ${SOURCES}/deploy ];
then
    echo "Not in sources root?"
    exit 1
fi

if [ ! -d ${APPROOT}/venv ]; then
    mkdir -p ${APPROOT}/venv
    virtualenv ${APPROOT}/venv
fi

echo "Create directories"
mkdir -p ${DJANGOROOT}          # ${APPROOT}/djangoproj
mkdir -p ${APPROOT}/web
mkdir -p ${APPROOT}/logs/uwsgi
mkdir -p ${APPROOT}/logs/web
mkdir -p ${APPROOT}/logs/app
mkdir -p ${APPROOT}/run

echo "Cleanup"
rm -rf ${DJANGOROOT}/*
rm -rf ${APPROOT}/web/*

echo "Placing files..."

echo "Deploy Django Project"
cp -r ${SOURCES}/*  ${DJANGOROOT}/
rm -rf ${DJANGOROOT}/deploy

echo "Deploy production setting.py"
cp /root/deploy/${APPNAME}/settings.py ${DJANGOROOT}/${APPNAME}/settings.py

echo "Rotate Django SECRET_KEY"
secret=$(date +%s | md5sum | base64)
perl -pi -e "s/SECRET_KEY = '[^\']*'/SECRET_KEY = '${secret}'/g" ${DJANGOROOT}/${APPNAME}/settings.py

echo "    create backlinks"
if [ -e ${DJANGOROOT}/logs ]
then
    rm -rf ${DJANGOROOT}/logs
fi

ln -s ${APPROOT}/logs ${DJANGOROOT}/

echo "Setting file righs"
chmod -R u=rwX ${APPROOT}
chmod -R go-rwxX ${APPROOT}
chown -R ${USER}:${USER} ${APPROOT}

echo "Switch environment"
sudo -u ${USER} /bin/bash - << venvpart
id
source ${APPROOT}/venv/bin/activate

echo "Update environment"
pip install -r requirements.txt

echo "Perform DB updates"

cd ${DJANGOROOT}
python2.7 manage.py makemigrations
python2.7 manage.py migrate

echo "Exit virtual environment"
deactivate
venvpart

echo "DONE Deployment to ${APPROOT} for ${APPNAME} (${USER})"
