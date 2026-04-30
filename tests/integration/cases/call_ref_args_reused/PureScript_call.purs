module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Val -> Unit
process _ _ = unit
repeated_var :: Val
repeated_var = PInt 1
single_var :: Val
single_var = PList [
    PInt 4,
    PInt 5,
    PInt 6
    ]


main :: Unit
main =
    let
        _ = process repeated_var (PInt 1)
        _ = process single_var (PInt 0)
        _ = process repeated_var (PInt 8)
    in
    unit
