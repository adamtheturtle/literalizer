module Fixture_json5_comment_scalar_Haskell where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
-- scalar heading
-- second heading line
my_data :: Val
my_data = 42  -- scalar inline
-- inline continuation
-- scalar trailing
main :: IO ()
main = seq my_data (return ())
