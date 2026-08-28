module Check where


import Prelude
process :: Val -> Unit
process _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = process (PList [
            PInt 1,
            PInt 2
            ])
        _ = process (PList [
            PInt 3
            ])
    in
    unit
