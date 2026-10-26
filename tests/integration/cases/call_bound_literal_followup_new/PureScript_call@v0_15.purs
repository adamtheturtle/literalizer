module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
make_widget :: Val -> Unit
make_widget _ = unit
consume :: Unit -> Unit
consume _ = unit
my_data = make_widget (PInt 42)


main :: Unit
main =
    let
        _ = consume my_data
    in
    unit
