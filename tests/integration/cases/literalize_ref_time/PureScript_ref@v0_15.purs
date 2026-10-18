module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


myTime :: Val
myTime = PStr "01:02:03"
my_data :: Val
my_data = PDict [
    (Tuple "x" (myTime))
]
