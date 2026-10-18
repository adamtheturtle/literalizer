module [main]

app_go : a, b -> {}
app_go = \_, _ -> {}

main =
    dbg (app_go (RList [RInt 1i128]) (RList [RStr "text"]))
    {}
