module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


shared :: Val
shared = PStr "s"
my_data :: Val
my_data = PDict [
    (Tuple "value" (shared))
]
