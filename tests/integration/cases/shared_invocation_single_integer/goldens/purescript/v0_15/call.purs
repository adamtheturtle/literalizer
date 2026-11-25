module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
consume :: Val -> Unit
consume _ = unit


main :: Unit
main =
    let
        _ = consume (PInt 1)
    in
    unit
