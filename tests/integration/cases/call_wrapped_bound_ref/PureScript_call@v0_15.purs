module Check where


import Prelude
data Val
    = PInt Int
make_widget :: Val -> Unit
make_widget _ = unit
value :: Val
value = PInt 1


main :: Unit
main =
    let
        _ = make_widget value
    in
    unit
