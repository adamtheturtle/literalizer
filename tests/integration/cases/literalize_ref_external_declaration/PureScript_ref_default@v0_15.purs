module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
consume_widget :: Val -> Unit
consume_widget _ = unit
shared :: Val
shared = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = shared


main :: Unit
main =
    let
        _ = consume_widget my_data
    in
    unit
