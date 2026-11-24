module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
make_widget :: Val -> Val -> Unit
make_widget _ _ = unit
consume :: Unit -> Val -> Unit
consume _ _ = unit
my_data = make_widget (PInt 42) (PInt 3)


main :: Unit
main =
    let
        _ = consume my_data (PInt 3)
    in
    unit
