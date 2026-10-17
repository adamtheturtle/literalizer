module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


existing :: Val
existing = PDict [
    (Tuple "_" (PStr "_"))
]
my_data :: Val
my_data = existing
