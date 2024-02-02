#!/bin/bash
#
# Setup and organize git repositories from a specific host

[[ -z "$GIT_HOST" ]] && declare -r GIT_HOST="github.com"
[[ -z "$GITLAB_HOME" ]] && declare -r GITLAB_HOME="$HOME/git/github"

function validate_args() {
    if [[ $# != 1 ]] ; then
        echo "One and only one argument is accepted" >&2
    elif ! grep -q "${GIT_HOST}" <<< "${1}" ; then
        echo "Provided HOST ${1} does not appear to be " \
             "from our expected host, ${GIT_HOST}" >&2
    else
        return 0
    fi
    return 1
}

function parse_path() {
    local -r url="$1"
    local path="${url#*${GIT_HOST}}"
    path="${path%.git}"
    path="${path:1}"
    echo $path
}

function main() {
    validate_args "$@" || return 1

    local -r url="$1"
    local -r path="$(parse_path ${url})"
    local -r full_path="${GITLAB_HOME}/${path}"
    if [[ -d "${full_path}/.git" ]] ; then
        echo "The directory ${full_path} already contains a repository !"
        return 1
    fi

    mkdir -p "${full_path}" && 
        cd "${full_path}" &&
        git init &&
        git remote add origin "$url" ||
        return 1
    echo "Repository '${url}' setup at '${full_path}'"
    echo 'A `git fetch` is required before work can begin'
}

if true ; then
    main "$@"
fi
