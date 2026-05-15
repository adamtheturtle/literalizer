module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "within_i32" (PStr "2024-01-15T12:00:00")),
    (Tuple "beyond_i32" (PStr "2099-06-15T08:30:00"))
    ]
