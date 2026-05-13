module Fixture_call_ref_args_heterogeneous_list_Haskell_call where
data Val = HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: Val -> Val -> IO ()
process _ _ = return ()
my_ints :: Val
my_ints = HList [
    1,
    2,
    3
    ]
my_strings :: Val
my_strings = HList [
    HStr "a",
    HStr "b"
    ]
my_empty :: Val
my_empty = HList []
main :: IO ()
main = do
    _ <- process my_ints (42)
    _ <- process my_strings (7)
    _ <- process my_empty (99)
    pure ()
