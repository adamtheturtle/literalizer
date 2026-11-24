module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    --
    -- document heading
    -- before the first entry
    -- after the key
    -- before the value
    ("counts", EList [
        -- before the first item
        EInt 1,  -- inline block after the comma
        -- before the second item
        EInt 2
        -- trailing inside the array
        ]),  -- after the nested collection
    ("more", EList [
        EInt 3,
        --
        -- block heading
        -- block continuation
        EInt 4  -- final inline
        ])
    -- trailing inside the object
    -- after the root
    -- after the document
    ]
