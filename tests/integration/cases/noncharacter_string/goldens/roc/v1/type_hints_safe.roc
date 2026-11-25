Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("fffe", RStr("\u(fffe)")),
    ("ffff", RStr("\u(ffff)")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
