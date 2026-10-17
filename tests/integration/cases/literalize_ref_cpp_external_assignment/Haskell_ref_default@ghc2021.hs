module Fixture_literalize_ref_cpp_external_assignment_Haskell_ref_default where
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
ref_data :: Val
ref_data = HList [
    1,
    2
    ]
my_data :: Val
my_data = HList [
    0
    ]
consume_widget my_data
my_data = ref_data
main :: IO ()
main = do
    _ <- consume_widget my_data
    pure ()
