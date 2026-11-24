module Fixture_jsonc_comment_positions_Haskell where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    --
    -- document heading
    -- before the first entry
    -- after the key
    -- before the value
    ("counts", HList [
        -- before the first item
        1,  -- inline block after the comma
        -- before the second item
        2
        -- trailing inside the array
        ]),  -- after the nested collection
    ("more", HList [
        3,
        --
        -- block heading
        -- block continuation
        4  -- final inline
        ])
    -- trailing inside the object
    -- after the root
    -- after the document
    ]
main :: IO ()
main = seq my_data (return ())
