module Fixture_rust_lazy_static_empty_sibling_Haskell where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
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
    ("a", HList [HList [1, 2], HList [3]]),
    ("b", HList [HList [], HList [1]])
    ]
main :: IO ()
main = seq my_data (return ())
