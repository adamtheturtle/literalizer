module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a-b" (PInt 1)),
    (Tuple "two words" (PInt 2)),
    (Tuple "she said \"hi\"" (PInt 3)),
    (Tuple "" (PInt 4)),
    (Tuple "valid_key" (PInt 5))
]
