module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Unit
process _ = unit
unknown_value :: Val
unknown_value = PList [
    PInt 1
    ]


main :: Unit
main =
    let
        _ = process unknown_value
    in
    unit
