module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "date" (PStr "2024-01-15")),
    (Tuple "datetime" (PStr "2024-01-15T12:30:00+00:00"))
    ]
