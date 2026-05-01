module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))
send :: Val -> Unit
send _ = unit


main :: Unit
main =
    let
        _ = send (PDict [(Tuple "a" (PInt 1)), (Tuple "b" (PStr "x"))])
    in
    unit
