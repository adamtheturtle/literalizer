Val := [
    RList(List(Val)),
]
consume_widget = |_| {}

item : Val
item = RList([])
my_data : Val
my_data = RList([
    item,
    item,
])

main! = |_args| {
    dbg (consume_widget(my_data))
    Ok({})
}
