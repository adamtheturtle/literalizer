module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
process :: Val -> Val -> Unit
process _ _ = unit
shared :: Val
shared = PInt 1
other :: Val
other = PInt 2


main :: Unit
main =
    let
        _ = process shared (PInt 1)
        _ = process other (PInt 0)
        _ = process shared (PInt 8)
    in
    unit
