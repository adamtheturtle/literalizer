module Fixture_zig_special_float_std_binding_scalar_Haskell where
data Val = HFloat Double
instance Num Val where
    fromInteger n = HFloat (fromIntegral n)
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HFloat f) = HFloat (negate f)
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
std :: Val
std = (0/0)
main :: IO ()
main = seq std (return ())
