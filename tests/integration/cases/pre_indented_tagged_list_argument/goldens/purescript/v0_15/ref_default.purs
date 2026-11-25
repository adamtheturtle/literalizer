module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
consume_widget :: Val -> Unit
consume_widget _ = unit


main :: Unit
main =
    let
        _ = consume_widget (    PList [
                PInt 1,
                PInt 2
            ])
    in
    unit
