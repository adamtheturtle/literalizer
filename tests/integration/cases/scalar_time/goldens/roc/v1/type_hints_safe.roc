Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("starts_at", RStr("09:30:00")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
