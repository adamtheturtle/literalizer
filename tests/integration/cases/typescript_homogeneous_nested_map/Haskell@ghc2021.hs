module Fixture_typescript_homogeneous_nested_map_Haskell where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
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
    ("first", HMap [("x", 1), ("y", 2)]),
    ("second", HMap [("z", 3)])
    ]
main :: IO ()
main = seq my_data (return ())
