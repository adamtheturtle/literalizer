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
my_var :: Val
my_var = PInt 42


main :: Unit
main =
    let
        _ = process (PDict [(Tuple "key" (my_var)), (Tuple "count" (PInt 42)), (Tuple "label" (PStr "example"))])
    in
    unit
