module Fixture_roundtrip_verifier_object_order_and_numeric_equivalence_Haskell where
data Val = HNull | HBool Bool | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger n = HFloat (fromIntegral n)
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("b", HNull),
    ("a", HMap [("y", HList [1.0]), ("x", HBool False)])
    ]
main :: IO ()
main = seq my_data (return ())
