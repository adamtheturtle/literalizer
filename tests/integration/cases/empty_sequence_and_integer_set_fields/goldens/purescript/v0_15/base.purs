module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
    | PSet (Array Val)


my_data :: Val
my_data = PDict [
    (Tuple "a" (PList [])),
    (Tuple "b" (PSet [PInt 1, PInt 2]))
]
