module Fixture_singleton_array_inference_context_Haskell where
data Val = HNull | HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
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
    ("nil", HList [HList [HList [HList [HList [HList [HList [HList [HList [HNull]]]]]]]]]),
    ("empty", HList [HList [HList [HList [HList [HList [HList [HList [HList [HList []]]]]]]]]]),
    ("siblings", HList [HList [HList [HList [HList [HList [HList [HList [HList [HList [4, 5]]]]]]]]]])
    ]
main :: IO ()
main = seq my_data (return ())
