module Check where


import Prelude
f :: Val -> Unit
f _ = unit
data Val
    = PList (Array Val)


main :: Unit
main =
    let
        _ = f (PList [])
    in
    unit
