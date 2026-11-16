Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

userObj : Val
userObj = RDict([
    ("_", RStr("_")),
])
my_data : Val
my_data = userObj

main! = |_args| {
    _ = my_data
    Ok({})
}
