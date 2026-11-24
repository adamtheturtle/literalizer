Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

key_binding : Val
key_binding = RDict([
    ("a", RInt(1.I128)),
])

main! = |_args| {
    _ = key_binding
    Ok({})
}
