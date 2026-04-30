module Fixture_call_ref_nested_in_list_Haskell_call where
data Val = HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: Val -> IO ()
process _ = return ()
my_var :: Val
my_var = 42
my_other :: Val
my_other = 7
main :: IO ()
main = do
    _ <- process(HList [my_var, 42, HStr "static"])
    _ <- process(HList [my_other, 7, HStr "label"])
    pure ()
