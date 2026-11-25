Val := [
    RInt(I128),
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RInt(1.I128)]),
    RList([RFloat(2.5.F64)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
