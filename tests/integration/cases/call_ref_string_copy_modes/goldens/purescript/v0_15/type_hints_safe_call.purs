module Check where


import Prelude
data Val
    = PStr String
    | PList (Array Val)
consume :: Val -> Unit
consume _ = unit
item :: Val
item = PStr "s"


main :: Unit
main =
    let
        _ = consume item
    in
    unit
