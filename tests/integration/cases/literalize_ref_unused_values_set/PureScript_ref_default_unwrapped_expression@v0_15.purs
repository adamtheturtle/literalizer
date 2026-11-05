module Check where


import Prelude
data Val
    = PInt Int
    | PSet (Array Val)
consume_widget :: Val -> Unit
consume_widget _ = unit


main :: Unit
main =
    let
        _ = consume_widget (PSet [
            PInt 1,
            PInt 2
        ])
    in
    unit
