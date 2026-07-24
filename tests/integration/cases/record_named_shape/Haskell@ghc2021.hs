module Fixture_record_named_shape_Haskell where
data Val = HBool Bool | HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HList [
    HMap [("id", 100), ("label", HStr "first entry"), ("enabled", HBool False), ("related_ids", HList [102, 103])],
    HMap [("id", 101), ("label", HStr "second entry"), ("enabled", HBool True), ("related_ids", HList [100])]
    ]
main :: IO ()
main = seq my_data (return ())
