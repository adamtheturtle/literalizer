module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "0a" (PStr "first")),
    (Tuple "1b" (PStr "second"))
    ]
