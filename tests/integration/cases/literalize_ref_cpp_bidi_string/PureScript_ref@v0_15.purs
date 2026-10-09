module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


text :: Val
text = PStr "a‪b"
my_data :: Val
my_data = PDict [
    (Tuple "value" (text))
]
