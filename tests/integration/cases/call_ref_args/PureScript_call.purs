module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Val -> Unit
process _ _ = unit
my_var :: Val
my_var = PList [
    PInt 1,
    PInt 2,
    PInt 3
    ]
my_other :: Val
my_other = PList [
    PInt 4,
    PInt 5,
    PInt 6
    ]


main :: Unit
main =
    let
        _ = process my_var (PInt 42)
        _ = process my_other (PInt 7)
    in
    unit
