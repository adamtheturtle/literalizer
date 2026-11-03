module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "lists" (PList [PList [PInt 1], PList [PStr "x"], PList []])),
    (Tuple "maps" (PList [PDict [(Tuple "x" (PInt 1))], PDict [(Tuple "x" (PStr "s"))]])),
    (Tuple "empties" (PDict [(Tuple "a" (PList [PInt 1])), (Tuple "b" (PList []))]))
]
