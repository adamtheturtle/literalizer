Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]
process = |_| {}

my_var : Val
my_var = RInt(42.I128)
my_other : Val
my_other = RInt(7.I128)

main! = |_args| {
    dbg (process(RList([my_var, RInt(42.I128), RStr("static")])))
    dbg (process(RList([my_other, RInt(7.I128), RStr("label")])))
    Ok({})
}
