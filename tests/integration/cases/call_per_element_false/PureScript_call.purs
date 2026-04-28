module Check where


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
