make_widget = |_| {}

my_data = make_widget(RList([
    RInt(1.I128),
]))

main! = |_args| {
    _ = my_data
    Ok({})
}
