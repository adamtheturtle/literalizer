thing_go = |_| {}

my_data = thing_go(RList([RInt(1.I128)]))

main! = |_args| {
    _ = my_data
    Ok({})
}
