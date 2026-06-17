module Check where


import Prelude
put :: Val -> Val -> Unit
put _ _ = unit
get :: Val -> Unit
get _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = put (PInt 1) (PInt 10)
        _ = get (PInt 1)
    in
    unit
