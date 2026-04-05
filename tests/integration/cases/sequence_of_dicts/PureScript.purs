module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "name" (PStr "Alice")), (Tuple "age" (PInt 30))],
    PDict [(Tuple "name" (PStr "Bob")), (Tuple "age" (PInt 25))]
    ]
