Val := [
    RNull,
    RList(List(Val)),
]
consume = |_| {}

my_null : Val
my_null = RNull
regular_null : Val
regular_null = RNull

main! = |_args| {
    dbg (consume(my_null))
    dbg (consume(regular_null))
    Ok({})
}
