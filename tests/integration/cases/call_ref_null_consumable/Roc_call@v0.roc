module [main]

Val : [
    RNull,
    RList (List Val),
]
consume : a -> {}
consume = \_ -> {}

my_null : Val
my_null = RNull
regular_null : Val
regular_null = RNull
main =
    dbg (consume my_null)
    dbg (consume regular_null)
    {}
