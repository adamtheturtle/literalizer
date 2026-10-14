module Check where


import Prelude
data Val
    = PInt Int
process :: Val -> Unit
process _ = unit
value :: Val
value = PInt 1


main :: Unit
main =
    let
        _ = process value
    in
    unit
