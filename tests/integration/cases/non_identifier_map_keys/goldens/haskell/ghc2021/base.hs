module Fixture_non_identifier_map_keys_Haskell where
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
    ("two words", 2),
    ("she said \"hi\"", 3),
    ("", 4),
    ("valid_key", 5)
    ]
main :: IO ()
main = seq my_data (return ())
