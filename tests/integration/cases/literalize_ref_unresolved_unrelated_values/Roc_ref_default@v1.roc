Val := [
    RInt(I128),
    RList(List(Val)),
]
consume_widget = |_| {}

a : Val
a = RInt(0.I128)
my_data : Val
my_data = RList([
    a,
    RInt(1.I128),
])

main! = |_args| {
    dbg (consume_widget(my_data))
    Ok({})
}
