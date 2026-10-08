module Fixture_literalize_ref_cpp_mixed_sibling_maps_Haskell_ref where
data Val = HNull | HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
actual :: Val
actual = 42
my_data :: Val
my_data = HList [
    HMap [("$ref", 1)],
    HMap [("$ref", HNull)],
    actual
    ]
main :: IO ()
main = seq my_data (return ())
