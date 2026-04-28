module Check where


data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Unit
process _ = unit
myVar :: Val
myVar = PList [
    PInt 1,
    PInt 2,
    PInt 3
    ]


main :: Unit
main =
    let
        _ = process myVar
    in
    unit
