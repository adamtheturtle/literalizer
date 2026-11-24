module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "b" (PDict [(Tuple "k" (PInt 1))])),
    (Tuple "a" (PDict [(Tuple "k" (PStr "2040-01-01T00:00:00+00:00"))]))
]
