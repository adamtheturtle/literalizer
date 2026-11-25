Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

allocator : Val
allocator = RDict([
    ("a", RInt(1.I128)),
])

main! = |_args| {
    _ = allocator
    Ok({})
}
