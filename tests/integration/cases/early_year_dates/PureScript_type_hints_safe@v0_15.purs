module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "date" (PStr "0099-05-27")),
    (Tuple "naive" (PStr "0001-01-01T12:30:00")),
    (Tuple "recent" (PStr "2024-05-27T10:00:00"))
]
