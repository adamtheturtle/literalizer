module Check where


import Data.Tuple (Tuple(..))
data Val
    = PNull
    | PBool Boolean
    | PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "name" PStr "Alice"),
    (Tuple "age" PInt 30),
    (Tuple "active" PBool true),
    (Tuple "score" PNull),
    (Tuple "joined" PStr "2024-01-15"),
    (Tuple "last_login" PStr "2024-01-15T12:30:00+00:00"),
    (Tuple "avatar" PStr "48656c6c6f")
    ]
