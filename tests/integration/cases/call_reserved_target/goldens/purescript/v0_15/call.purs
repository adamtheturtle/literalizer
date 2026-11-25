module Check where


import Prelude
data Val
    = PStr String
    | PList (Array Val)
op :: Val -> Unit
op _ = unit


main :: Unit
main =
    let
        _ = op (PStr "hello")
    in
    unit
