module Check where


data Tuple a b = Tuple a b
data Val
    = PNull
    | PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "outer" (PDict [(Tuple "a" (PInt 1)), (Tuple "b" (PStr "x")), (Tuple "c" (PNull))]))
    ]
