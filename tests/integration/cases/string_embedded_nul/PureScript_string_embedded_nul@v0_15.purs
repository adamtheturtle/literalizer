module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "x" (PStr "\x00")),
    (Tuple "y" (PStr "\x00\x31"))
    ]
