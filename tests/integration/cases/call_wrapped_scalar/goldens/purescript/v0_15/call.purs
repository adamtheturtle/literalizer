module Check where


import Prelude
make_widget :: Val -> Unit
make_widget _ = unit
data Val
    = PInt Int


main :: Unit
main =
    let
        _ = make_widget (PInt 1)
    in
    unit
