module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "scores" (PList [PInt 10, PInt 20, PInt 30])),
    (Tuple "args" (PList [PInt 1, PStr "email", PStr "a@gmail.com", PInt 100]))
    ]
