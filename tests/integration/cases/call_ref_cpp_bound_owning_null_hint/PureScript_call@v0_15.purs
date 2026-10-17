module Check where


import Prelude
data Val
    = PNull
    | PInt Int
    | PList (Array Val)
consume :: Val -> Unit
consume _ = unit
item :: Val
item = PList [
    PInt 1,
    PInt 2
]


main :: Unit
main =
    let
        _ = consume item
    in
    unit
