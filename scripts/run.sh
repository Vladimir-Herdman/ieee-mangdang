#TDOO: STILL IN DEVELOPMENT`
#!/usr/bin/env bash
#To use this script, go to the directory the files

cd_pyscript_dir() {
    local pyscript_path path
    pyscript_path="$1"
    if [[ ! $pyscript_path =~ / ]]; then printf './'; return; fi
    path="${pyscript_path%/*}"
    printf '%s' "$path"
}

get_pyfile_name() {
    true;
}

cleanup() {
    printf 'test'
}

main() {
    trap cleanup EXIT

    local pyscript
    pyscript="$1"
    cd "$(cd_pyscript_dir "$pyscript")" || exit 1

    #run background scripts to allow dogbot to move from keyboard commands

    #run passed pyscript while the two scripts are in background
    uv run python "$(get_pyfile_name "$pyscript")"
}

main "$1"
