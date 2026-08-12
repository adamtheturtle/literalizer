module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" (PDict [
        -- inner note
        (Tuple "b" (PInt 1))  -- inline b
        ])),
    (Tuple "list" (PList [
        PInt 1,  -- first
        PInt 2  -- second
        ]))
    ]
