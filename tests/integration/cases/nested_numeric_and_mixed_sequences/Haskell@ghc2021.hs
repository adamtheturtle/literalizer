module Fixture_nested_numeric_and_mixed_sequences_Haskell where
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
    ("numbers", HList [1, 2]),
    ("nested", HMap [("inner", HList [3])]),
    ("mixed", HList [4, HStr "five"])
    ]
main :: IO ()
main = seq my_data (return ())
