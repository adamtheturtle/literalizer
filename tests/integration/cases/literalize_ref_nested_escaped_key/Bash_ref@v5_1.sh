declare -A foo=(
    ["_"]="_"
)
declare -A my_data=(
    ["items"]="(\"([\\\"other\\\"]=1)\" \"foo\")"
    ["mapping"]="([\"value\"]=foo)"
)
