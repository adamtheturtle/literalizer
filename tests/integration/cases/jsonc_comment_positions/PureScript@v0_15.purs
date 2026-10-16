module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    --
    -- document heading
    -- before the first entry
    -- after the key
    -- before the value
    (Tuple "counts" (PList [
        -- before the first item
        PInt 1,  -- inline block after the comma
        -- before the second item
        PInt 2
        -- trailing inside the array
    ])),  -- after the nested collection
    (Tuple "more" (PList [
        PInt 3,
        --
        -- block heading
        -- block continuation
        PInt 4  -- final inline
    ]))
    -- trailing inside the object
    -- after the root
    -- after the document
]
