module Fixture_call_ref_args_trivial_register_Haskell_call where
data Val = HBool Bool | HInt Integer | HFloat Double | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
process :: Val -> Val -> IO ()
process _ _ = return ()
my_int :: Val
my_int = 1
my_bool :: Val
my_bool = HBool True
my_float :: Val
my_float = 3.14
my_list :: Val
my_list = HList [
    1,
    2,
    3
    ]
main :: IO ()
main = do
    _ <- process my_int (42)
    _ <- process my_bool (7)
    _ <- process my_float (9)
    _ <- process my_list (1)
    pure ()
