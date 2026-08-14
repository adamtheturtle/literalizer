module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "explicit_string" (PStr "5")),
    (Tuple "six" (PStr "explicitly tagged key"))
    ]
