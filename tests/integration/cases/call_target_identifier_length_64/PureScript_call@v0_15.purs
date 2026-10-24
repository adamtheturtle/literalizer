module Check where


import Prelude
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff :: Val -> Unit
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (PInt 1)
    in
    unit
