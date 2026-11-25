module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PLong Number
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" (PDict [(Tuple "k" (PLong 2208988800.0))])),
    (Tuple "b" (PDict [(Tuple "k" (PInt 1))]))
]
