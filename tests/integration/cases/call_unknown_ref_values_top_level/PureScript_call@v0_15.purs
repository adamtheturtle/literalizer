module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Unit
process _ = unit
known_value :: Val
known_value = PInt 1
unknown_value :: Val
unknown_value = PList []


main :: Unit
main =
    let
        _ = process unknown_value
    in
    unit
