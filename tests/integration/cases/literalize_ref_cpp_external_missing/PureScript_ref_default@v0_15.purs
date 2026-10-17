module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
consume_widget :: Val -> Unit
consume_widget _ = unit
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
consume_widget my_data
my_data = item


main :: Unit
main =
    let
        _ = consume_widget my_data
    in
    unit
