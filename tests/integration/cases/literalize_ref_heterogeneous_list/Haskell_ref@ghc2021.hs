module Fixture_literalize_ref_heterogeneous_list_Haskell_ref where
data Val = HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
one :: Val
one = 1
two :: Val
two = HStr "s"
my_data :: Val
my_data = HList [
    one,
    two
    ]
main :: IO ()
main = seq my_data (return ())
