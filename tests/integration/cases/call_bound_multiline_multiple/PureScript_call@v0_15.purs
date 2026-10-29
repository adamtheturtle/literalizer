module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
f :: Val -> Unit
f _ = unit
ref_data :: Val
ref_data = PList [
    PInt 1,
    PInt 2
]


main :: Unit
main =
    let
        _ = f (PList [
            ref_data
        ])
        _ = f (PList [
            ref_data
        ])
    in
    unit
