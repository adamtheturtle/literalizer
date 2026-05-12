module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "users" (PList [
        PDict [
            (Tuple "name" (PStr "Bob")),
            (Tuple "tags" (PList [
                PStr "admin",
                PStr "user"
                ]))
            ],
        PDict [
            (Tuple "name" (PStr "Carol")),
            (Tuple "tags" (PList [
                PStr "guest"
                ]))
            ]
        ]))
    ]
