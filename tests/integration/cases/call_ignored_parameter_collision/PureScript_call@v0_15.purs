module Check where


import Prelude
f :: Val -> Val -> Unit
f _ _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = f (PInt 1) (PInt 2)
    in
    unit
