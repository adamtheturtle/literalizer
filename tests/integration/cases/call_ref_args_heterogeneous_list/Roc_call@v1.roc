Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]
process = |_, _| {}

my_ints : Val
my_ints = RList([
    RInt(1.I128),
    RInt(2.I128),
    RInt(3.I128),
])
my_strings : Val
my_strings = RList([
    RStr("a"),
    RStr("b"),
])
my_empty : Val
my_empty = RList([])

main! = |_args| {
    dbg (process(my_ints, RInt(42.I128)))
    dbg (process(my_strings, RInt(7.I128)))
    dbg (process(my_empty, RInt(99.I128)))
    Ok({})
}
