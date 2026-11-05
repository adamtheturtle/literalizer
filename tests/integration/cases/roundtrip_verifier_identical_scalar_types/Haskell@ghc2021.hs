module Fixture_roundtrip_verifier_identical_scalar_types_Haskell where
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
    ("value", HList [HBool True, HBool False, 0, 1])
    ]
main :: IO ()
main = seq my_data (return ())
