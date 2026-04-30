module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


x :: Val
x = PDict [
    (Tuple "_" (PStr "_"))
    ]
my_data :: Val
my_data = PList [
    x,
    PInt 1,
    PInt 2
    ]
