Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("key", RStr("\"bang!\"")),  # real
])

main! = |_args| {
    _ = my_data
    Ok({})
}
