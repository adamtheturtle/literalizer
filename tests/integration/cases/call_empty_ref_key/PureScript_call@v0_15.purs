module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
consume :: Val -> Unit
consume _ = unit
external_value :: Val
external_value = PInt 1


main :: Unit
main =
    let
        _ = consume external_value
    in
    unit
