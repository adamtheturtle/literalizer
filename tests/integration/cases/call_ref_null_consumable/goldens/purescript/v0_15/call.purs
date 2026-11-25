module Check where


import Prelude
data Val
    = PNull
    | PList (Array Val)
consume :: Val -> Unit
consume _ = unit
my_null :: Val
my_null = PNull
regular_null :: Val
regular_null = PNull


main :: Unit
main =
    let
        _ = consume my_null
        _ = consume regular_null
    in
    unit
