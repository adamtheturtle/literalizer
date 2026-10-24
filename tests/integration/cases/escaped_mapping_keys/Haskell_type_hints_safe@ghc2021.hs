module Fixture_escaped_mapping_keys_Haskell_type_hints_safe where
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
    ("quote\"backslash\\", 1),
    ("line\nbreak", 2),
    ("$(literal)${text}", 3),
    ("RStr prefix", 4)
    ]
main :: IO ()
main = seq my_data (return ())
