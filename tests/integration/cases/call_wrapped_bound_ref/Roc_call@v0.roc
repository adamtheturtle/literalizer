module [main]

Val : [
    RInt I128,
]
make_widget : a -> {}
make_widget = \_ -> {}

value : Val
value = RInt 1i128
main =
    dbg (make_widget value)
    {}
