module Check where


import Prelude
do_thing :: Val -> Unit
do_thing _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = do_thing (PInt 1)
        _ = do_thing (PInt 2)
    in
    unit
