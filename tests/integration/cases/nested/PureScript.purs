module Check where


import Data.Tuple (Tuple(..))
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "users" PList [PDict [(Tuple "name" PStr "Bob"), (Tuple "tags" PList [PStr "admin", PStr "user"])], PDict [(Tuple "name" PStr "Carol"), (Tuple "tags" PList [PStr "guest"])]])
    ]
