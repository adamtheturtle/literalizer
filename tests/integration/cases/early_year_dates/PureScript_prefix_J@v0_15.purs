module Check where


data Tuple a b = Tuple a b
data Val
    = JStr String
    | JDict (Array (Tuple String Val))


my_data :: Val
my_data = JDict [
    (Tuple "date" (JStr "0099-05-27")),
    (Tuple "naive" (JStr "0001-01-01T12:30:00")),
    (Tuple "recent" (JStr "2024-05-27T10:00:00"))
]
