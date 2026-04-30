module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
process :: Val -> Unit
process _ = unit
myVar :: Val
myVar = PInt 42


main :: Unit
main =
    let
        _ = process (PList [PDict [(Tuple "ref" (PStr "myVar"))], PInt 42, PStr "static"])
    in
    unit
