module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
consume :: Val -> Unit
consume _ = unit
item :: Val
item = PInt 42


main :: Unit
main =
    let
        _ = consume (PDict [(Tuple "field" (item))])
    in
    unit
