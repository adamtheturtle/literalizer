module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PList [PDict [(Tuple "name" (PStr "Alice"))], PDict [(Tuple "name" (PStr "Bob"))]],
    PList [PDict [(Tuple "name" (PStr "Charlie"))], PDict [(Tuple "name" (PStr "Dave"))]]
    ]
