module Check where


data Tuple a b = Tuple a b
data Val
    = JNull
    | JBool Boolean
    | JInt Int
    | JStr String
    | JDict (Array (Tuple String Val))


my_data :: Val
my_data = JDict [
    (Tuple "name" (JStr "Alice")),
    (Tuple "age" (JInt 30)),
    (Tuple "active" (JBool true)),
    (Tuple "score" (JNull))
    ]
