module Check where


import Prelude
process :: Val -> Unit
process _ = unit
data Val
    = PInt Int


main :: Unit
main =
    let
        _ = process (PInt 42)
    in
    unit
