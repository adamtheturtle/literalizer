module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "first" (PInt 1))],
    PDict [(Tuple "repeated" (PStr "a"))],
    PDict [(Tuple "repeated" (PStr "b"))]
]
