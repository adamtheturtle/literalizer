module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


userObj :: Val
userObj = PDict [
    (Tuple "_" (PStr "_"))
    ]
my_data :: Val
my_data = userObj
