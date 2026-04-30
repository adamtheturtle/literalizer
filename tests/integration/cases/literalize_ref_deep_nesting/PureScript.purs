module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" (PDict [(Tuple "b" (PDict [(Tuple "c" (PDict [(Tuple "$ref" (PStr "deep"))]))]))]))
    ]
