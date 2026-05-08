module Check where


import Prelude
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
process :: Val -> Val -> Unit
process _ _ = unit
my_ints :: Val
my_ints = PList [
    PInt 1,
    PInt 2,
    PInt 3
    ]
my_strings :: Val
my_strings = PList [
    PStr "a",
    PStr "b"
    ]


main :: Unit
main =
    let
        _ = process my_ints (PInt 42)
        _ = process my_strings (PInt 7)
    in
    unit
