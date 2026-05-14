module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Unit
process _ = unit
existing :: Val
existing = PInt 42


main :: Unit
main =
    let
        _ = process existing
    in
    unit
