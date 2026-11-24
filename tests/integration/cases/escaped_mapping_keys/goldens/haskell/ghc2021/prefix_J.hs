module Fixture_escaped_mapping_keys_Haskell_prefix_J where
data Val = JInt Integer | JStr String | JMap [(String, Val)]
instance Num Val where
    fromInteger = JInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (JInt n) = JInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = JMap [
    ("quote\"backslash\\", 1),
    ("line\nbreak", 2),
    ("$(literal)${text}", 3),
    ("RStr prefix", 4)
    ]
main :: IO ()
main = seq my_data (return ())
