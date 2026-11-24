module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


shared_time :: Val
shared_time = PStr "12:30:15+02:00"
my_data :: Val
my_data = PDict [
    (Tuple "x" (shared_time))
]
