module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "scores" (PList [PInt 1, PInt 2]))],
    PDict [(Tuple "scores" (PList [PInt 3, PInt 4]))]
]
