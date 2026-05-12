module Fixture_int_list_Haskell_type_hints_safe_seq_tuple where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: (Val, Val, Val)
my_data = (
    1,
    2,
    3
    )
main :: IO ()
main = seq my_data (return ())
