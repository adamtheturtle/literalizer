module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    {- { - and { - stay readable -}
    {- balanced { - nested - } and trailing - } stay readable -}
    (Tuple "x" (PInt 1))
]
