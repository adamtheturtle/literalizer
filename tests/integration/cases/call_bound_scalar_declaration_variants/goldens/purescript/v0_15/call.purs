module Check where


import Prelude
data Val
    = PInt Int
consume :: Val -> Unit
consume _ = unit
shared :: Val
shared = PInt 42


main :: Unit
main =
    let
        _ = consume shared
    in
    unit
