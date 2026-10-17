module [main]

app_client_go : a, b -> {}
app_client_go = \_, _ -> {}

main =
    dbg (app_client_go (RList [RInt 1i128]) (RList [RStr "text"]))
    {}
