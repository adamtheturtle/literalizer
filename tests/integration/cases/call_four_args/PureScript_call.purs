module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Val -> Val -> Val -> Unit
process _ _ _ _ = unit


main :: Unit
main =
    let
        _ = process (PInt 1) (PInt 2) (PInt 3) (PInt 4)
        _ = process (PInt 10) (PInt 20) (PInt 30) (PInt 40)
    in
    unit
