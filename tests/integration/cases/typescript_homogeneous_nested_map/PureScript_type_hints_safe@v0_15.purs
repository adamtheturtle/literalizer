module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "first" (PDict [(Tuple "x" (PInt 1)), (Tuple "y" (PInt 2))])),
    (Tuple "second" (PDict [(Tuple "z" (PInt 3))]))
]
