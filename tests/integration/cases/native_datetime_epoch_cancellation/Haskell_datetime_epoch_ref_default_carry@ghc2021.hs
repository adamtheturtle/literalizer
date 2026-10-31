module Fixture_native_datetime_epoch_cancellation_Haskell_datetime_epoch_ref_default_carry where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
stamp :: Val
stamp = 1
result_data :: Val
result_data = stamp
main :: IO ()
main = seq result_data (return ())
