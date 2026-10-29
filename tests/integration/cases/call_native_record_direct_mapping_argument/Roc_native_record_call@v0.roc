module [main]

consume : a -> {}
consume = \_ -> {}

main =
    dbg (consume ({ name: "Ada" }))
    {}
