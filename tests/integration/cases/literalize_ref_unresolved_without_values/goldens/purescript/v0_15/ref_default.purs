module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
consume_widget :: Val -> Unit
consume_widget _ = unit
a :: Val
a = PInt 0
my_data :: Val
my_data = PList [
    a,
    PInt 1
]


main :: Unit
main =
    let
        _ = consume_widget my_data
    in
    unit
