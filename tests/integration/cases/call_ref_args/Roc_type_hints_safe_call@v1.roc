Val := [
    RInt(I128),
    RList(List(Val)),
]
process = |_, _| {}

my_var : Val
my_var = RList([
    RInt(1.I128),
    RInt(2.I128),
    RInt(3.I128),
])
my_other : Val
my_other = RList([
    RInt(4.I128),
    RInt(5.I128),
    RInt(6.I128),
])

main! = |_args| {
    dbg (process(my_var, RInt(42.I128)))
    dbg (process(my_other, RInt(7.I128)))
    Ok({})
}
