process = |_| {}

my_data = process(RInt(1.I128))

main! = |_args| {
    _ = my_data
    Ok({})
}
