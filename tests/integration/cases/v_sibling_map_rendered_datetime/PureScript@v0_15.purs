module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" (PDict [(Tuple "k" (PStr "2020-01-01T00:00:00+00:00"))])),
    (Tuple "b" (PDict [(Tuple "k" (PStr "string"))]))
]
