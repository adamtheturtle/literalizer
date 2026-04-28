module Check where


data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Val -> Unit
process _ _ = unit


main :: Unit
main =
    let
        _ = process (PInt 1) (PInt 42)
        _ = process (PInt 2) (PInt 100)
    in
    unit
