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


main :: Unit
main =
    let
        _ = process (PDict [(Tuple "value" (PInt 1))])
        _ = process (PDict [(Tuple "value" (PStr "hello"))])
    in
    unit
