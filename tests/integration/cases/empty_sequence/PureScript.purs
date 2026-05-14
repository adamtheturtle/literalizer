module Check where


data Tuple a b = Tuple a b
data Val
    = PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PList [],
    PDict []
    ]
