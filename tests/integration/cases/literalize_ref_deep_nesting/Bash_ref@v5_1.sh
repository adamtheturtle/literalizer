declare deep=(
    "(1 2)"
    "(3 4)"
)
declare -A my_data=(
    ["a"]="([\"b\"]=\"([\\\"c\\\"]=deep)\")"
)
