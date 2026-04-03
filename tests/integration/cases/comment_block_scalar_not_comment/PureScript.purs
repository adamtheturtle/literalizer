module Check where


import Data.Tuple (Tuple(..))
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "description" PStr "# not a comment\n"),
    (Tuple "name" PStr "foo")
    ]
