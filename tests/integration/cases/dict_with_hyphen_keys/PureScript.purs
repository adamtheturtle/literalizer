module Check where


import Data.Tuple (Tuple(..))
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "my-key" PStr "value1"),
    (Tuple "another-key" PStr "value2"),
    (Tuple "normal_key" PStr "value3")
    ]
