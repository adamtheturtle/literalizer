module Fixture_cpp_record_in_variant_Haskell where
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
my_data = HMap [
    ("h", HList [1, HStr "a", HList [2, HStr "b"], HMap [("k", HList [HBool True])]])
    ]
main :: IO ()
main = seq my_data (return ())
