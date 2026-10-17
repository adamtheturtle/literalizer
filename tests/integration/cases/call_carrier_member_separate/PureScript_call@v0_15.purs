module Check where


import Prelude
app :: { go :: Val -> Val -> Unit }
app = { go: \_ _ -> unit }
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


main :: Unit
main =
    let
        _ = app.go (PList [PInt 1]) (PList [PStr "text"])
    in
    unit
