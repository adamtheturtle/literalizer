Val := [
    RInt(I128),
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(1.I128),
    RFloat(2.5.F64),
    RInt(3.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
