declare -A deep=(
    ["_"]="_"
)
declare -A my_data=(
    ["a"]="([\"b\"]=\"([\\\"c\\\"]=deep)\")"
)
