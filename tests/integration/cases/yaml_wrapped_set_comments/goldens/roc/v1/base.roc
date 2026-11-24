Val := [
    RInt(I128),
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([
    RInt(10.I128),  # comment for ten
    RInt(2.I128),  # comment for two
])

main! = |_args| {
    _ = my_data
    Ok({})
}
