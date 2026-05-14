module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "times" (PList [PStr "09:30:00", PStr "17:45:00", PStr "23:59:59"]))
    ]
