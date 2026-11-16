Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("value", RDict([("$ref", RStr("foo"))])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
