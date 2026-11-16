make_widget = |_| {}

my_data = make_widget(RStr("text"))

main! = |_args| {
    _ = my_data
    Ok({})
}
