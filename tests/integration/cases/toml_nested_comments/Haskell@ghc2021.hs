module Fixture_toml_nested_comments_Haskell where
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
    -- About the first dotted key.
    -- About the second dotted key.
    ("dotted", HMap [("first", 1), ("second", 2)]),
    ("plain", 3),  -- About the plain key.
    -- Inside the table.
    ("table", HMap [("inner", 4)]),
    -- Before the first entry.
    -- Before the second entry.
    ("entries", HList [HMap [("name", HStr "one")], HMap [("name", HStr "two")]])
    ]
main :: IO ()
main = seq my_data (return ())
