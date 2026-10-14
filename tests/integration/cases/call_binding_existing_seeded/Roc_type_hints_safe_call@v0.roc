module [main]

Val : [
    RInt I128,
]
make_widget : a -> {}
make_widget = \_ -> {}

my_data = make_widget (RInt 42i128)
my_data = make_widget my_data
main =
    dbg (make_widget my_data)
    {}
