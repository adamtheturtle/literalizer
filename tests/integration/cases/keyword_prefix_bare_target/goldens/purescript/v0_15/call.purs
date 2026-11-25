module Check where


import Prelude
first_value :: Val -> Unit
first_value _ = unit
data Val
    = PInt Int


main :: Unit
main =
    let
        _ = first_value (PInt 1)
    in
    unit
