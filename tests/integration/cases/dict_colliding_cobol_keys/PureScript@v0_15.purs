module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "user_name" (PInt 1)),
    (Tuple "user.name" (PInt 2)),
    (Tuple "user-name" (PInt 3)),
    (Tuple "field_name_that_is_really_quite_long_one" (PInt 4)),
    (Tuple "field_name_that_is_really_quite_long_two" (PInt 5))
    ]
