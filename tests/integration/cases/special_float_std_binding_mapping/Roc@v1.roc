Val := [
    RFloat(F64),
    RStr(Str),
    RDict(List((Str, Val))),
]

std : Val
std = RDict([
    ("nan", RFloat(F64.nan)),
    ("positive", RFloat(F64.infinity)),
    ("negative", RFloat(-F64.infinity)),
])

main! = |_args| {
    _ = std
    Ok({})
}
