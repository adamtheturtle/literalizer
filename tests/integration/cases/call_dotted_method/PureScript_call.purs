module Check where


data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
app :: { client :: { fetch :: Val -> Unit } }
app = { client: { fetch: \_ -> unit } }


main :: Unit
main =
    let
        _ = app.client.fetch (PStr "hello")
        _ = app.client.fetch (PInt 42)
        _ = app.client.fetch (PBool true)
    in
    unit
