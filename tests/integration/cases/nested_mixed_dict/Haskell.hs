module Fixture_nested_mixed_dict_Haskell where
data Val = HNull | HInt Integer | HStr String | HMap [(String, Val)]
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
    ("outer", HMap [("a", 1), ("b", HStr "x"), ("c", HNull)])
    ]
