module Fixture_pair_sequence_Haskell_type_hints_safe_date_iso where
data Val = HInt Integer | HStr String | HList [Val]
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
    1,
    HStr "hello"
    ]
main :: IO ()
main = seq my_data (return ())
