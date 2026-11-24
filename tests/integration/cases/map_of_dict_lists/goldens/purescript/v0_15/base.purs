module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" (PList [PDict [(Tuple "k" (PInt 1))]])),
    (Tuple "b" (PList [PDict [(Tuple "k" (PInt 2))]]))
]
