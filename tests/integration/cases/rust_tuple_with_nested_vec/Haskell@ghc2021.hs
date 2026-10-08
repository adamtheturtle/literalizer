module Fixture_rust_tuple_with_nested_vec_Haskell where
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
    ("lint", HList [2, HList []]),
    ("test", HList [5, HList [HStr "compile"]]),
    ("package", HList [7, HList [HStr "link", HStr "test"]])
    ]
main :: IO ()
main = seq my_data (return ())
