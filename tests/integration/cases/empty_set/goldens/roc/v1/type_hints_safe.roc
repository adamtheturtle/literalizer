Val := [
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([])

main! = |_args| {
    _ = my_data
    Ok({})
}
