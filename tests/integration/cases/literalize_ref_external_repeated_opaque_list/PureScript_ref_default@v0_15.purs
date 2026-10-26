module Check where


import Prelude
data Val
    = PList (Array Val)
consume_widget :: Val -> Unit
consume_widget _ = unit
item :: Val
item = PList []
my_data :: Val
my_data = PList [
    item,
    item
]


main :: Unit
main =
    let
        _ = consume_widget my_data
    in
    unit
