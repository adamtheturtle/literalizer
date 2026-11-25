module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "first" (PDict [(Tuple "items" (PList [PInt 1, PDict [(Tuple "value" (PInt 2))]]))])),
    (Tuple "second" (PDict [(Tuple "items" (PList [PInt 1, PDict [(Tuple "value" (PStr "s"))]]))]))
]
