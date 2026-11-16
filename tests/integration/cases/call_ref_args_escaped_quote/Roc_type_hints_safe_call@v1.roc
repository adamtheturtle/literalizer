Val := [
    RStr(Str),
    RList(List(Val)),
]
process = |_| {}

my_str : Val
my_str = RStr("a\"b")

main! = |_args| {
    dbg (process(my_str))
    Ok({})
}
