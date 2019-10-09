#!/usr/bin/env bash

while [[ true ]]
do
    printf "\n"
    read -e -p "- Select Directus directory path:" GF_DIR
    cleared_path=$(echo ${GF_DIR} | sed 's#~/#@home@/#g')
    if [[ ${cleared_path} =~ "@home@" ]];
    then
        new_path="$(echo "$HOME")$( echo ${cleared_path} | sed 's#@home@##g')"
    else
        new_path=${cleared_path}
    fi
    echo ${new_path}
    if [[ -d ${new_path} ]]
    then
        if [[ -d "${new_path}/config" && -f "${new_path}/public/admin/config.js" ]]
        then
            echo "${new_path}" > data/tmp/directusEnv.txt
            break
        fi
    fi
    tput setaf 1; echo -e  "\nNo valid Directus environment, try again..."
    tput sgr0;

done
