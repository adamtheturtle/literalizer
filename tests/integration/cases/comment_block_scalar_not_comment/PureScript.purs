module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "description" (PStr "# not a comment\n")),
    (Tuple "name" (PStr "foo"))
    ]
