module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "exact_millisecond" (PStr "09:30:15.123000")),
    (Tuple "sub_millisecond" (PStr "09:30:15.123456"))
    ]
