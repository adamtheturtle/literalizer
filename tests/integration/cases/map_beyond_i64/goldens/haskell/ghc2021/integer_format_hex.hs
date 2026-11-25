module Fixture_map_beyond_i64_Haskell_integer_format_hex where
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
    ("a", 0x7fffffffffffffff),
    ("b", 0x8000000000000000)
    ]
main :: IO ()
main = seq my_data (return ())
