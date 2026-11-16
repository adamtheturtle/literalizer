Val := [
    RFloat(F64),
]

std : Val
std = RFloat(F64.nan)

main! = |_args| {
    _ = std
    Ok({})
}
