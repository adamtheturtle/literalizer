module [main]

Val : [
    RInt I128,
    RList (List Val),
]
make_widget : a, b -> {}
make_widget = \_, _ -> {}
consume : a, b -> {}
consume = \_, _ -> {}

my_data = make_widget (RInt 42i128) (RInt 3i128)
main =
    dbg (consume (RInt 3i128) my_data)
    {}
