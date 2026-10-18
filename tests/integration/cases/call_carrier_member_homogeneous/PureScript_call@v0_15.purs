module Check where


import Prelude
app :: { go :: Val -> Val -> Unit }
app = { go: \_ _ -> unit }
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = app.go (PList [PInt 1]) (PList [PInt 2])
    in
    unit
