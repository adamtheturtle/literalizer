module Check where


import Prelude
store_item :: Val -> Val -> Unit
store_item _ _ = unit
read_item :: Val -> Unit
read_item _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = store_item (PInt 1) (PInt 10)
        _ = read_item (PInt 1)
    in
    unit
