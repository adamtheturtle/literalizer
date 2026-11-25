module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "nested" (PDict [(Tuple "times" (PList [PStr "1900-01-01T00:00:00+00:00"]))]))],
    PDict []
]
