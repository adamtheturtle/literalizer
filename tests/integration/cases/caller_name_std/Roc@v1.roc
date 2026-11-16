Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

std : Val
std = RDict([
    ("a", RInt(1.I128)),
])

main! = |_args| {
    _ = std
    Ok({})
}
