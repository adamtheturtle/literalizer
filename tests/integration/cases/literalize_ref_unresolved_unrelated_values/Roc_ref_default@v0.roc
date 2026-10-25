module [main]

Val : [
    RInt I128,
    RList (List Val),
]
consume_widget : a -> {}
consume_widget = \_ -> {}

a : Val
a = RInt 0i128
my_data : Val
my_data = RList [
    a,
    RInt 1i128,
]
main =
    dbg (consume_widget my_data)
    {}
