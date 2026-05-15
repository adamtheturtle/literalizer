module Fixture_tuple_record_field_Haskell where
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
    ("call", HStr "send"),
    ("args", HList [1, HStr "email", HStr "a@gmail.com", 100])
    ]
main :: IO ()
main = seq my_data (return ())
