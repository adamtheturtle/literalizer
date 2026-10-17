module Fixture_literalize_ref_cpp_external_missing_Haskell_ref_default where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
consume_widget :: a -> IO ()
consume_widget _ = return ()
item :: Val
item = HList [
    1,
    2
    ]
my_data :: Val
my_data = HList [
    1,
    2
    ]
consume_widget my_data
my_data = item
main :: IO ()
main = do
    _ <- consume_widget my_data
    pure ()
