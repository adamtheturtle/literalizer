make_widget = |_| {}

my_data = make_widget(RList([RList([RInt(1.I128), RInt(2.I128)]), RList([RInt(3.I128)])]))

main! = |_args| {
    _ = my_data
    Ok({})
}
