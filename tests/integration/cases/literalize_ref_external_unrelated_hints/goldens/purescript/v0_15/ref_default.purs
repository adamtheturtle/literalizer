module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
consume_widget :: Val -> Unit
consume_widget _ = unit
missing :: Val
missing = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = missing


main :: Unit
main =
    let
        _ = consume_widget my_data
    in
    unit
