module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "filled" (PList [PInt 1, PStr "value"])),
    (Tuple "empty" (PList []))
]
