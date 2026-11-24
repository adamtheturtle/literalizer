module Check where


import Prelude
f :: Val -> Unit
f _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = f (PInt 1)
    in
    unit
