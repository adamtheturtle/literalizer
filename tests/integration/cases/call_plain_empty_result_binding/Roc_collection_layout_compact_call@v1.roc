make_widget = |_| {}

my_data = make_widget(RList([]))

main! = |_args| {
    _ = my_data
    Ok({})
}
