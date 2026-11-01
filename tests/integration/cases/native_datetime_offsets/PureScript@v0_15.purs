module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "stamps" (PList [PStr "2001-02-03T04:05:06+00:00:01", PStr "2001-02-03T04:05:06-00:00:01", PStr "2001-02-03T04:05:06+00:00:00.000001", PStr "2001-02-03T04:05:06-00:00:00.000001", PStr "2001-02-03T04:05:06+05:30:15.000001", PStr "2001-02-03T04:05:06-05:30:15.000001"]))
]
