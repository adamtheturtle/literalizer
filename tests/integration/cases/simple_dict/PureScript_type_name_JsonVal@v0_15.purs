module Check where


data Tuple a b = Tuple a b
data JsonVal
    = PNull
    | PBool Boolean
    | PInt Int
    | PStr String
    | PDict (Array (Tuple String JsonVal))


my_data :: JsonVal
my_data = PDict [
    (Tuple "name" (PStr "Alice")),
    (Tuple "age" (PInt 30)),
    (Tuple "active" (PBool true)),
    (Tuple "score" (PNull))
    ]
