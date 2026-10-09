module Fixture_literalize_ref_null_bound_list_hint_Haskell_ref where
data Val = HNull | HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
myValue :: Val
myValue = HNull
my_data :: Val
my_data = myValue
main :: IO ()
main = seq my_data (return ())
