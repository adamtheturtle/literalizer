module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


user_obj :: Val
user_obj = PDict [
    (Tuple "_" (PStr "_"))
]
my_data :: Val
my_data = user_obj
