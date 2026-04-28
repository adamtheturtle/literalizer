module Fixture_comment_scalar_Haskell where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
-- note
my_data :: Val
my_data = 42
main :: IO ()
main = seq my_data (return ())
