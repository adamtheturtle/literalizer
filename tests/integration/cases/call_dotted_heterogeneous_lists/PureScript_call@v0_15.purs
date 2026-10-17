module Check where


import Prelude
app :: { client :: { go :: Val -> Val -> Unit } }
app = { client: { go: \_ _ -> unit } }
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


main :: Unit
main =
    let
        _ = app.client.go (PList [PInt 1]) (PList [PStr "text"])
    in
    unit
