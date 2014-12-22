#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./create-sources VERSION"
    exit 1
fi

VERSION=${1}
NAME="thredds"

git clone git://github.com/Unidata/${NAME}

(
 cd ${NAME}
 git checkout -b v${VERSION}
)

mv ./${NAME} ./${NAME}-${VERSION}
find ./${NAME}-${VERSION} -name "*.jar" -delete
find ./${NAME}-${VERSION} -name "*.class" -delete
find ./${NAME}-${VERSION} -name "*.dll" -delete
find ./${NAME}-${VERSION} -name "*.zip" -delete

# Remove unused files
rm -Rf ./${NAME}-${VERSION}/docs/*
rm -Rf ./${NAME}-${VERSION}/lib
rm -Rf ./${NAME}-${VERSION}/cdm/doc
rm -Rf ./${NAME}-${VERSION}/opendap/doc/*
# Unwanted ... for now
rm -Rf ./${NAME}-${VERSION}/cdm-test
rm -Rf ./${NAME}-${VERSION}/opendap
rm -Rf ./${NAME}-${VERSION}/ldm
rm -Rf ./${NAME}-${VERSION}/ui
rm -Rf ./${NAME}-${VERSION}/ncIdv
rm -Rf ./${NAME}-${VERSION}/visad
rm -Rf ./${NAME}-${VERSION}/tds
rm -Rf ./${NAME}-${VERSION}/it
rm -Rf ./${NAME}-${VERSION}/cdmvalidator
rm -Rf ./${NAME}-${VERSION}/dts
rm -Rf ./${NAME}-${VERSION}/grib
rm -Rf ./${NAME}-${VERSION}/tdm
rm -Rf ./${NAME}-${VERSION}/wmotables
rm -Rf ./${NAME}-${VERSION}/wmoTablesOld
rm -Rf ./${NAME}-${VERSION}/.git
find ./${NAME}-${VERSION} -name ".git*" -delete
tar cJf ${NAME}-${VERSION}-clean.tar.xz ./${NAME}-${VERSION}