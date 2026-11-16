Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]
process = |_| {}

my_var : Val
my_var = RInt(42.I128)

main! = |_args| {
    dbg (process(RList([my_var, RInt(42.I128), RStr("static")])))
    Ok({})
}
