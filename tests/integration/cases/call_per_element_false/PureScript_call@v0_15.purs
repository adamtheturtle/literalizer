module Check where


import Prelude
data Val
    = PInt Int
process :: Val -> Unit
process _ = unit


main :: Unit
main =
    let
        _ = process (PInt 1)
    in
    unit
