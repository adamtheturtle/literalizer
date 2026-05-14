module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "id" (PInt 1)),
    (Tuple "owner" (PDict [(Tuple "name" (PStr "Alice")), (Tuple "age" (PInt 30))]))
    ]
