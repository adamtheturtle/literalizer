module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
ref_data :: Val
ref_data = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = PList [
    PInt 0
]


main :: Unit
main =
    let
        _ = (void)my_data;
        _ = my_data = ref_data
        _ = (void)my_data;
    in
    unit
