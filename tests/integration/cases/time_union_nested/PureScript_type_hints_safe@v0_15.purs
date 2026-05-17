module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "mixed" (PList [PList [PStr "09:30:00"], PList []]))
    ]
