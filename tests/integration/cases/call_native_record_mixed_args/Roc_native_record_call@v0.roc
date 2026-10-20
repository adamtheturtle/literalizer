module [main]

consume : a, b, c -> {}
consume = \_, _, _ -> {}

main =
    dbg (consume ({ x: 1i128 }) (2i128) ("first"))
    dbg (consume ({ name: "Ada" }) (3i128) ("second"))
    {}
