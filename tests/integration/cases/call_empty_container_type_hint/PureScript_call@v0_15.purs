module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
process :: Val -> Val -> Unit
process _ _ = unit


main :: Unit
main =
    let
        _ = process (PList [PInt 1, PDict []]) (PInt 42)
    in
    unit
