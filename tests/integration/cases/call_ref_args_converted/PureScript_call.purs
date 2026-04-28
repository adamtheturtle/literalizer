module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Val -> Unit
process _ _ = unit
myVar :: Val
myVar = PList [
    PInt 1,
    PInt 2,
    PInt 3
    ]
myOther :: Val
myOther = PList [
    PInt 4,
    PInt 5,
    PInt 6
    ]


main :: Unit
main =
    let
        _ = process myVar (PInt 42)
        _ = process myOther (PInt 7)
    in
    unit
