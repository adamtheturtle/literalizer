module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "groups" (PList [PList [PDict [(Tuple "id" (PInt 1))]], PList [PDict [(Tuple "id" (PInt 2))]]]))
]
