module Fixture_cobol_collision_generated_suffix_Haskell where
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
    ("a-b", 1),
    ("a b", 2),
    ("a-b-2", 3)
    ]
main :: IO ()
main = seq my_data (return ())
