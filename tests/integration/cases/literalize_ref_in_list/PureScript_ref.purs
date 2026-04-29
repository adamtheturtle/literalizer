module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


x :: Val
x = PInt 0
y :: Val
y = PInt 0
my_data :: Val
my_data = PList [
    x,
    y
    ]
