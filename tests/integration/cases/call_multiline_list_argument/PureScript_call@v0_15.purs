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
        _ =     PInt 1,
        _ =     PInt 2
        _ =     ])
        _ = process (PList [
        _ =     PInt 3
        _ =     ])
    in
    unit
