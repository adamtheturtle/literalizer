module Check where


import Prelude
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
process :: Val -> Unit
process _ = unit


main :: Unit
main =
    let
        _ = process (PList [PInt 1, PStr "x"])
    in
    unit
