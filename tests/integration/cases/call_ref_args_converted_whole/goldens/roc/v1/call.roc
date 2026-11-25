Val := [
    RInt(I128),
    RList(List(Val)),
]
process = |_| {}

my_var : Val
my_var = RList([
    RInt(1.I128),
    RInt(2.I128),
    RInt(3.I128),
])

main! = |_args| {
    dbg (process(my_var))
    Ok({})
}
