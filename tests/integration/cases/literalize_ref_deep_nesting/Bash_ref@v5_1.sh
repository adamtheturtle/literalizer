declare deep=(
    "(\"one\" \"two\")"
    "(\"three\" \"four\")"
)
declare -A my_data=(
    ["a"]="([\"b\"]=\"([\\\"c\\\"]=deep)\")"
)
