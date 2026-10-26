module [main]

Val : [
    RInt I128,
    RList (List Val),
]
make_widget : a -> {}
make_widget = \_ -> {}
consume : a -> {}
consume = \_ -> {}

my_data = make_widget (RInt 42i128)
main =
    dbg (consume my_data)
    {}
