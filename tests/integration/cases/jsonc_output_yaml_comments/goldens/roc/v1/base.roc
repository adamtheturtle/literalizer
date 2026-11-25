Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # server
    ("host", RStr("localhost")),  # default
])

main! = |_args| {
    _ = my_data
    Ok({})
}
