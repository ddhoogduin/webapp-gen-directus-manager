#!/usr/bin/env bash

while [[ true ]]
do
    printf "\n"
    read -e -p "- Select Directus directory path:" GF_DIR
    cleared_path=$(echo ${GF_DIR} | sed 's#~/#@home@/#g')
    if [[ ${cleared_path} =~ "@home@" ]];
    then
        new_path="$(echo "$HOME")$( echo ${cleared_path} | sed 's#@home@##g')"
    fi

    if [[ -d ${new_path} ]]
    then
        if [[ -d "${new_path}/config" && -f "${new_path}/public/admin/config.js" ]]
        then
            mkdir -p data/tmp
            echo "${new_path}" > data/tmp/directusEnv.txt
            break
        fi
    else
        printf  "\nX No valid Directus environment, try again...\n"
    fi
done
