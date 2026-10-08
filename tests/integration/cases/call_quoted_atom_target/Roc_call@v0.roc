module [main]

DoThing : a -> {}
DoThing = \_ -> {}

main =
    dbg (DoThing (RInt 1i128))
    dbg (DoThing (RInt 2i128))
    {}
