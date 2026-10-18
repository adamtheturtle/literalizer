module Check where


import Prelude
make_widget :: Val -> Val -> Unit
make_widget _ _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = make_widget (PList [PInt 1]) (PList [PInt 2])
    in
    unit
