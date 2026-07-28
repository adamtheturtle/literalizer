module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
process :: Val -> Unit
process _ = unit
my_list :: Val
my_list = PDict [
    (Tuple "unused" (PStr "value"))
    ]


main :: Unit
main =
    let
        _ = process (PList [PList [PDict [(Tuple "inner" (my_list))]]])
    in
    unit
