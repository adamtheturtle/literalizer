module [main]

Val : [
    RList (List Val),
]
consume_widget : a -> {}
consume_widget = \_ -> {}

item : Val
item = RList []
my_data : Val
my_data = RList [
    item,
    item,
]
main =
    dbg (consume_widget my_data)
    {}
