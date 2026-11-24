Val := [
    RInt(I128),
    RList(List(Val)),
]
consume_widget = |_| {}

shared : Val
shared = RList([
    RInt(1.I128),
    RInt(2.I128),
])
my_data : Val
my_data = shared

main! = |_args| {
    dbg (consume_widget(my_data))
    Ok({})
}
