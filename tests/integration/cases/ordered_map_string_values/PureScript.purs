module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "first" (PStr "one")),
    (Tuple "second" (PStr "two")),
    (Tuple "third" (PStr "three"))
    ]
