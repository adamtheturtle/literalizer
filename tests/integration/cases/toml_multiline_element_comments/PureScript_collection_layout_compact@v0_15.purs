module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "first" (PList [PInt 1, PInt 2])),
    (Tuple "second" (PInt 3))  -- About the second key.
    ]
