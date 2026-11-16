Val := [
    RInt(I128),
    RList(List(Val)),
]
consume_widget = |_| {}

missing : Val
missing = RList([
    RInt(1.I128),
    RInt(2.I128),
])
my_data : Val
my_data = missing

main! = |_args| {
    dbg (consume_widget(my_data))
    Ok({})
}
