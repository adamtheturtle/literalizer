module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
f :: Val -> Unit
f _ = unit
x :: Val
x = PList [
    PList [
        PInt 1,
        PInt 2
    ],
    PList [
        PInt 3,
        PInt 4
    ]
]


main :: Unit
main =
    let
        _ = f (PList [
            PList [
                x
            ]
        ])
    in
    unit
