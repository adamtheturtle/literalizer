module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Unit
process _ = unit


main :: Unit
main =
    let
        _ = process (PInt (-1))
        _ = process (PInt (-2))
        _ = process (PInt (-3))
    in
    unit
