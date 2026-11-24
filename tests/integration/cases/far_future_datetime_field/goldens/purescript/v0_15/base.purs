module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "ts" (PStr "3000-12-31T23:59:59.999999+00:00"))
]
