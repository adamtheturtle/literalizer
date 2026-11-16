Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

bound : Val
bound = RInt(2.I128)
my_data : Val
my_data = RDict([
    ("value", bound),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
