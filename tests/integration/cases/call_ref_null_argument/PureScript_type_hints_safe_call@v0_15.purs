module Check where


import Prelude
data Val
    = PNull
consume :: Val -> Unit
consume _ = unit
value :: Val
value = PNull


main :: Unit
main =
    let
        _ = consume value
    in
    unit
