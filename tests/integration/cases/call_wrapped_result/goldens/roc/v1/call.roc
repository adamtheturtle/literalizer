make_widget = |_| {}

my_data = make_widget(RInt(1.I128))

main! = |_args| {
    _ = my_data
    Ok({})
}
