module Fixture_rust_tuple_empty_sibling_slot_Haskell where
data Val = HInt Integer | HList [Val]
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
    HList [1, HList []],
    HList [2, HList [3]]
    ]
main :: IO ()
main = seq my_data (return ())
