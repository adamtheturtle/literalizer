module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "assert" (PInt 1)),
    (Tuple "else" (PInt 1)),
    (Tuple "error" (PInt 1)),
    (Tuple "false" (PInt 1)),
    (Tuple "for" (PInt 1)),
    (Tuple "function" (PInt 1)),
    (Tuple "if" (PInt 1)),
    (Tuple "import" (PInt 1)),
    (Tuple "importbin" (PInt 1)),
    (Tuple "importstr" (PInt 1)),
    (Tuple "in" (PInt 1)),
    (Tuple "local" (PInt 1)),
    (Tuple "null" (PInt 1)),
    (Tuple "self" (PInt 1)),
    (Tuple "super" (PInt 1)),
    (Tuple "tailstrict" (PInt 1)),
    (Tuple "then" (PInt 1)),
    (Tuple "true" (PInt 1)),
    (Tuple "ordinary" (PInt 1))
    ]
