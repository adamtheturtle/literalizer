module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))
process :: Val -> Unit
process _ = unit


main :: Unit
main =
    let
        _ = process (PDict [(Tuple "a" (PInt 1)), (Tuple "b" (PStr "x"))])
    in
    unit
