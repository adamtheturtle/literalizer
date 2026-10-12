module Fixture_literalize_ref_rust_repeated_nested_Haskell_ref where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
shared :: Val
shared = HList [
    1,
    2
    ]
my_data :: Val
my_data = HList [
    HMap [("left", shared), ("right", shared)]
    ]
main :: IO ()
main = seq my_data (return ())
