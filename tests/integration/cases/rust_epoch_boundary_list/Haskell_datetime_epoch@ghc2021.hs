module Fixture_rust_epoch_boundary_list_Haskell_datetime_epoch where
data Val = HList [Val] | HInt Integer
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
    -2147483649,
    -2147483648,
    2147483647,
    2147483648
    ]
main :: IO ()
main = seq my_data (return ())
