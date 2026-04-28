module Check where


import Prelude
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
app :: { client :: { fetch :: Val -> Unit } }
app = { client: { fetch: \_ -> unit } }
emit :: forall a. a -> Unit
emit _ = unit


main :: Unit
main =
    let
        _ = emit(app.client.fetch (PStr "hello"))
        _ = emit(app.client.fetch (PInt 42))
        _ = emit(app.client.fetch (PBool true))
    in
    unit
