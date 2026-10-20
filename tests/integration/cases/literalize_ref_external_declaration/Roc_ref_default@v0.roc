module [main]

Val : [
    RInt I128,
    RList (List Val),
]
consume_widget : a -> {}
consume_widget = \_ -> {}

shared : Val
shared = RList [
    RInt 1i128,
    RInt 2i128,
]
my_data : Val
my_data = shared
main =
    dbg (consume_widget my_data)
    {}
