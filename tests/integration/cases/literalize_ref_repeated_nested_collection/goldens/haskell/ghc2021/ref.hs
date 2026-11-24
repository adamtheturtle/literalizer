module Fixture_literalize_ref_repeated_nested_collection_Haskell_ref where
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
    HList [1, 2],
    HMap [("value", 1)]
    ]
my_data :: Val
my_data = HList [
    shared,
    shared
    ]
main :: IO ()
main = seq my_data (return ())
