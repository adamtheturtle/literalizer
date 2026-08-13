module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


deep :: Val
deep = PList [
    PList [
        PInt 1,
        PInt 2
        ],
    PList [
        PInt 3,
        PInt 4
        ]
    ]
my_data :: Val
my_data = PDict [
    (Tuple "a" (PDict [
        (Tuple "b" (PDict [
            (Tuple "c" (deep))
            ]))
        ]))
    ]
