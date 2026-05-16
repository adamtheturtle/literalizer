module Check where


import Prelude
process :: Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Val -> Unit
process _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ = unit
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = process (PInt 0) (PInt 1) (PInt 2) (PInt 3) (PInt 4) (PInt 5) (PInt 6) (PInt 7) (PInt 8) (PInt 9) (PInt 10) (PInt 11) (PInt 12) (PInt 13) (PInt 14) (PInt 15) (PInt 16) (PInt 17) (PInt 18) (PInt 19) (PInt 20) (PInt 21) (PInt 22) (PInt 23) (PInt 24) (PInt 25) (PInt 26)
    in
    unit
