module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" (PDict [
        (Tuple "b" (PList [PInt 1])),
        -- Outdented from the sequence, so the inner mapping claims this.
        (Tuple "c" (PInt 2))
        ])),
    -- Outdented from the inner mapping too, so the root claims this.
    (Tuple "d" (PInt 3))
    ]
