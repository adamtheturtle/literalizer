module Check where


import Prelude
data Val
    = PStr String
    | PList (Array Val)
app :: { client :: { fetch :: Val -> Unit } }
app = { client: { fetch: \_ -> unit } }


main :: Unit
main =
    let
        _ = app.client.fetch (PStr "hello")
        _ = app.client.fetch (PStr "world")
    in
    unit
