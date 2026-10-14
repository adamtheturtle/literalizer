module Check where


import Prelude
data Val
    = PInt Int
make_widget :: Val -> Unit
make_widget _ = unit
my_data = make_widget (PInt 42)
my_data = make_widget my_data


main :: Unit
main =
    let
        _ = make_widget my_data
    in
    unit
