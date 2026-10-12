module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PLong Number
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "within_i32" (PInt 1705320000)),
    (Tuple "beyond_i32" (PLong 4085195400.0))
]
