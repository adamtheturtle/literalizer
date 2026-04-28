module Fixture_uniform_mixed_num_dicts_in_seq_Haskell where
data Val = HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = HList [
    HMap [("x", 1), ("y", 2.5)],
    HMap [("x", 3), ("y", 4.0)]
    ]
