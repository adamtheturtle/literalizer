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
        _ = f (PList [PInt 1, PInt 2])
    in
    unit
