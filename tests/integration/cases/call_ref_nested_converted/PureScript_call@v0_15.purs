module Check where


import Prelude
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
process :: Val -> Unit
process _ = unit
myVar :: Val
myVar = PInt 42


main :: Unit
main =
    let
        _ = process (PList [myVar, PInt 42, PStr "static"])
    in
    unit
