module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "level1" (PDict [(Tuple "level2" (PDict [(Tuple "level3" (PDict [(Tuple "level4" (PDict [(Tuple "value" (PStr "deep")), (Tuple "items" (PList [PStr "a", PStr "b"]))]))])), (Tuple "sibling" (PInt 42))])), (Tuple "tags" (PList [PDict [(Tuple "name" (PStr "tag1")), (Tuple "meta" (PDict [(Tuple "priority" (PInt 1)), (Tuple "labels" (PList [PStr "x", PStr "y"]))]))]]))]))
    ]
