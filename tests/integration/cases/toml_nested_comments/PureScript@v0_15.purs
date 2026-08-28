module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    -- About the first dotted key.
    -- About the second dotted key.
    (Tuple "dotted" (PDict [(Tuple "first" (PInt 1)), (Tuple "second" (PInt 2))])),
    (Tuple "plain" (PInt 3)),  -- About the plain key.
    -- Before the first entry.
    -- Before the second entry.
    (Tuple "entries" (PList [PDict [(Tuple "name" (PStr "one"))], PDict [(Tuple "name" (PStr "two"))]])),
    -- Inside the table.
    (Tuple "table" (PDict [(Tuple "inner" (PInt 4))]))
    ]
