module Check where


import Prelude
process :: Val -> Val -> Unit
process _ _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = process (PInt 1) (PInt 2)
    in
    unit
