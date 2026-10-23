module Check where


import Prelude
data Val
    = PNull
consume :: Val -> Unit
consume _ = unit
item :: Val
item = PNull


main :: Unit
main =
    let
        _ = consume item
    in
    unit
