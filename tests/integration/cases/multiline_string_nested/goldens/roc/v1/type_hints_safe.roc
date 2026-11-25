Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("outer", RList([RList([RStr("nested first line\n  indented\n\nnested last line\n")])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
