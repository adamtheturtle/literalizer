module Fixture_nested_positional_empty_lists_reversed_Haskell_type_hints_safe where
data Val = HInt Integer | HList [Val]
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
    HList [HList [1]],
    HList [HList []]
    ]
main :: IO ()
main = seq my_data (return ())
