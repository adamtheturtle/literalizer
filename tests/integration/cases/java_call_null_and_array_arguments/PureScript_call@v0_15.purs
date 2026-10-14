module Check where


import Prelude
data Val
    = PNull
    | PInt Int
    | PList (Array Val)
process :: Val -> Unit
process _ = unit


main :: Unit
main =
    let
        _ = process (PNull)
        _ = process (PList [PInt 1, PInt 2])
    in
    unit
