#!/usr/bin/env bash

while [[ true ]]
do
    printf "\n"
    read -e -p "- Select an output path:" GF_DIR
    cleared_path=$(echo ${GF_DIR} | sed 's#~/#@home@/#g')
    if [[ ${cleared_path} =~ "@home@" ]];
    then
        new_path="$(echo "$HOME")$( echo ${cleared_path} | sed 's#@home@##g')"
    fi

    if [[ -d ${new_path} ]]
    then
            echo "${new_path}" > data/tmp/outPath.txt
            break
    fi
done
