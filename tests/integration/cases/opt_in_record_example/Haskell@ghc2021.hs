module Fixture_opt_in_record_example_Haskell where
data Val = HBool Bool | HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
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
    ("name", HStr "Ada"),
    ("active", HBool True),
    ("scores", HList [1, 2, 3])
    ]
main :: IO ()
main = seq my_data (return ())
