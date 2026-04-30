module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


deep :: Val
deep = PDict [
    (Tuple "_" (PStr "_"))
    ]
my_data :: Val
my_data = PDict [
    (Tuple "a" (PDict [(Tuple "b" (PDict [(Tuple "c" (deep))]))]))
    ]
