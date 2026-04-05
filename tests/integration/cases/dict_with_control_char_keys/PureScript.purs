module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "key\nwith\nnewlines" (PStr "value1")),
    (Tuple "key\twith\ttabs" (PStr "value2")),
    (Tuple "" (PStr "value3"))
    ]
