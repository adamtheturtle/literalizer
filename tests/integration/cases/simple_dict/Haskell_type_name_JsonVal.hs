module Fixture_simple_dict_Haskell_type_name_JsonVal where
data JsonVal = HNull | HBool Bool | HInt Integer | HStr String | HMap [(String, JsonVal)]
instance Num JsonVal where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: JsonVal
my_data = HMap [
    ("name", HStr "Alice"),
    ("age", 30),
    ("active", HBool True),
    ("score", HNull)
    ]
