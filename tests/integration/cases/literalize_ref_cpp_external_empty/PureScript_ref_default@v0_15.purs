module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
item :: Val
item = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = PList [
    PInt 1,
    PInt 2
]


main :: Unit
main =
    let
        _ = (void)my_data;
        _ = my_data = item
        _ = (void)my_data;
    in
    unit
