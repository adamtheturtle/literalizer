Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("user_name", RInt(1.I128)),
    ("user.name", RInt(2.I128)),
    ("user-name", RInt(3.I128)),
    ("field_name_that_is_really_quite_long_one", RInt(4.I128)),
    ("field_name_that_is_really_quite_long_two", RInt(5.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
