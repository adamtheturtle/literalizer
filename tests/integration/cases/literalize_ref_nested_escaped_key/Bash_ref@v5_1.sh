declare -A foo=(
    ["_"]="_"
)
declare -A my_data=(
    ["mapping"]="([\"value\"]=foo)"
    ["items"]="(\"([\\\"other\\\"]=1)\" \"foo\")"
)
