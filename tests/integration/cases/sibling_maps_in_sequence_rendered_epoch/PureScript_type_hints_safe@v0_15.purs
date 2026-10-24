module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "k" (PStr "2040-01-01T00:00:00+00:00"))],
    PDict [(Tuple "k" (PInt 1))]
]
