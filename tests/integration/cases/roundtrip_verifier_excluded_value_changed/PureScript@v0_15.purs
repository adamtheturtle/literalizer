module Check where


data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "keep" (PBool true)),
    (Tuple "skip" (PBool false))
]
