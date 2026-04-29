module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


myVar :: Val
myVar = PInt 0
my_data :: Val
my_data = PDict [
    (Tuple "key" (myVar))
    ]
