module Check where


import Prelude
process :: Val -> Unit
process _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = process (PInt 1)
    in
    unit
