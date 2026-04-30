module Fixture_call_ref_nested_in_dict_Haskell where
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
my_data = HList [
    HList [HMap [("key", HMap [("$ref", HStr "my_var")]), ("count", 42)]]
    ]
main :: IO ()
main = seq my_data (return ())
