module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "user" (PDict [(Tuple "id" (PInt 1)), (Tuple "name" (PStr "Alice"))])),
    (Tuple "project" (PDict [(Tuple "title" (PStr "report")), (Tuple "tags" (PList [PStr "draft", PStr "urgent"]))]))
    ]
