Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RFloat(F64.infinity),
    RFloat(-F64.infinity),
    RFloat(F64.nan),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
