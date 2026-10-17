module Check where


import Prelude
data Val
    = PNull
    | PList (Array Val)
consume_widget :: Val -> Unit
consume_widget _ = unit
item :: Val
item = PNull
my_data :: Val
my_data = PNull
consume_widget my_data
my_data = item


main :: Unit
main =
    let
        _ = consume_widget my_data
    in
    unit
