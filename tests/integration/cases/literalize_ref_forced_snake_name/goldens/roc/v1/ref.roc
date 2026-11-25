Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

user_obj : Val
user_obj = RDict([
    ("_", RStr("_")),
])
my_data : Val
my_data = user_obj

main! = |_args| {
    _ = my_data
    Ok({})
}
