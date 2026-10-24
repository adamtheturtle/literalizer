module Fixture_dict_colliding_normalized_long_keys_Haskell_integer_format_hex where
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
    ("a_b", 0x1),
    ("a-b", 0x2),
    ("averyveryverylongkeynamethatgoesonandonandon", 0x3),
    ("averyveryverylongkeynamethatgoesonandmore", 0x4)
    ]
main :: IO ()
main = seq my_data (return ())
