module Check where


import Prelude
data Val
    = PBool Boolean
    | PInt Int
    | PFloat Number
    | PList (Array Val)
process :: Val -> Val -> Unit
process _ _ = unit
my_int :: Val
my_int = PInt 1
my_bool :: Val
my_bool = PBool true
my_float :: Val
my_float = PFloat 3.14
my_list :: Val
my_list = PList [
    PInt 1,
    PInt 2,
    PInt 3
    ]


main :: Unit
main =
    let
        _ = process my_int (PInt 42)
        _ = process my_bool (PInt 7)
        _ = process my_float (PInt 9)
        _ = process my_list (PInt 1)
    in
    unit
