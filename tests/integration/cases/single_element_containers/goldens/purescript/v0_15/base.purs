module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "single_map" (PList [PDict []])),
    (Tuple "single_list" (PList [PList [PInt 1]])),
    (Tuple "single_deep" (PList [PList [PList [PInt 2]]]))
]
