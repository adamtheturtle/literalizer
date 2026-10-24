{-# LANGUAGE BinaryLiterals #-}
module Fixture_dict_colliding_normalized_long_keys_Haskell_integer_format_binary where
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
    ("a_b", 0b1),
    ("a-b", 0b10),
    ("averyveryverylongkeynamethatgoesonandonandon", 0b11),
    ("averyveryverylongkeynamethatgoesonandmore", 0b100)
    ]
main :: IO ()
main = seq my_data (return ())
