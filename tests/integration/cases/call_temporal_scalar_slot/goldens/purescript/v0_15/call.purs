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
        _ = process (PStr "09:30:00")
        _ = process (PStr "2024-01-15T00:00:00+00:00")
        _ = process (PInt 1)
    in
    unit
