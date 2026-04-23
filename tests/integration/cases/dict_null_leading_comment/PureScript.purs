module Check where


data Tuple a b = Tuple a b
data Val
    = PNull
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    -- comment
    (Tuple "name" (PStr "Alice")),
    (Tuple "score" (PNull))
    ]
