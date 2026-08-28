module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "flow" (PList [
        PInt 1,
        -- After the first element.
        PInt 2
        ])),
    -- Between the key and its value.
    (Tuple "gap" (PInt 3)),
    -- On the block scalar header.
    (Tuple "block" (PStr "Text.\n")),
    (Tuple "nested" (PList [
        PInt 1,
        PInt 1
        -- On the nested alias.
        ])),
    (Tuple "anchored" (PInt 4)),
    (Tuple "alias" (PInt 4))
    -- On the alias.
    ]
