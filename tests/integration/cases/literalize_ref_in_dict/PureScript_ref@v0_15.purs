module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


myVar :: Val
myVar = PInt 1
my_data :: Val
my_data = PDict [
    (Tuple "key" (myVar))
    ]
