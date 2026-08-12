module Fixture_yaml_nested_comments_Haskell where
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
    ("a", HMap [
        -- inner note
        ("b", 1)  -- inline b
        ]),
    ("list", HList [
        1,  -- first
        2  -- second
        ])
    ]
main :: IO ()
main = seq my_data (return ())
