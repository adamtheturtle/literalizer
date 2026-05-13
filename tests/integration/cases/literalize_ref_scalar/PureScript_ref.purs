module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


myInt :: Val
myInt = PInt 42
my_data :: Val
my_data = myInt
