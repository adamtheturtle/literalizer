process = |_, _| {}

my_data = process(RInt(1.I128), RInt(2.I128))

main! = |_args| {
    _ = my_data
    Ok({})
}
