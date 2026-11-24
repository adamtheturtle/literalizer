Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("long_str", RStr("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")),
    ("quoted", RStr("a\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"b")),
    ("wide", RStr("中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
