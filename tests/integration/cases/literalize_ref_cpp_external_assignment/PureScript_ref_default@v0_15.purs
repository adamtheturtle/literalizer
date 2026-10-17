module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
consume_widget :: Val -> Unit
consume_widget _ = unit
ref_data :: Val
ref_data = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = PList [
    PInt 0
]
consume_widget my_data
my_data = ref_data


main :: Unit
main =
    let
        _ = consume_widget my_data
    in
    unit
