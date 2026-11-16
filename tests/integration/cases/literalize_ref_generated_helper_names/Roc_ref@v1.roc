Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

std : Val
std = RDict([
    ("a", RInt(1.I128)),
])
arena : Val
arena = RDict([
    ("a", RInt(1.I128)),
])
allocator : Val
allocator = RDict([
    ("a", RInt(1.I128)),
])
my_data : Val
my_data = RList([
    std,
    arena,
    allocator,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
