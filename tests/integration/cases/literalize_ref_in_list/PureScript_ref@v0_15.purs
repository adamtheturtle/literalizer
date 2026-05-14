module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


valX :: Val
valX = PDict [
    (Tuple "_" (PStr "_"))
    ]
valY :: Val
valY = PDict [
    (Tuple "_" (PStr "_"))
    ]
my_data :: Val
my_data = PList [
    valX,
    valY
    ]
