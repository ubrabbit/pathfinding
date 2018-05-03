#!/bin/bash

make
RESULT=$?
if [ "${RESULT}" != "0" ]; then
    echo "build failure"
    exit 2
fi

cp -f c_path.so ./path_ui/c_path.so
echo "build success"
