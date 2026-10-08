module [main]

app_client_consume : a, b -> {}
app_client_consume = \_, _ -> {}

main =
    dbg (app_client_consume ({ x: 1i128 }) (2i128))
    dbg (app_client_consume ({ name: "Ada" }) (3i128))
    {}
