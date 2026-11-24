Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("morning", RStr("09:30:00")),
    ("afternoon", RStr("14:15:00")),
    ("evening", RStr("23:59:59")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
