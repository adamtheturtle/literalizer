module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" (PList [
        PInt 1,
        PInt 2,
        PInt 3
        ])),  -- inline a
    (Tuple "b" (PInt 2))  -- inline b
    ]
