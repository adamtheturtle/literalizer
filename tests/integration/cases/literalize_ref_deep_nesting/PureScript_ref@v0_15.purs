module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


deep :: Val
deep = PList [
    PList [
        PStr "one",
        PStr "two"
        ],
    PList [
        PStr "three",
        PStr "four"
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
