module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
process :: Val -> Unit
process _ = unit
big_list :: Val
big_list = PList [
    PStr "x"
    ]


main :: Unit
main =
    let
        _ = process (PDict [(Tuple "m" (big_list))])
    in
    unit
