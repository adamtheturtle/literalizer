declare -A my_var=(
    ["_"]="_"
)
declare -A item_var=(
    ["_"]="_"
)
declare -A my_data=(
    ["key"]=my_var
    ["items"]="(\"item_var\" \"([\\\"fallback\\\"]=\\\"value\\\")\")"
)
