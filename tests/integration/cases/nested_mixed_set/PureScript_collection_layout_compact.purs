module Check where


data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))
    | PSet (Array Val)


my_data :: Val
my_data = PDict [
    (Tuple "name" (PStr "Alice")),
    (Tuple "tags" (PSet [PBool true, PInt 42, PStr "apple"]))
    ]
