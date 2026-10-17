module Fixture_systemverilog_keyword_prefix_parameter_Haskell_call where
make_widget :: Val -> IO ()
make_widget _ = return ()
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
main :: IO ()
main = do
    _ <- make_widget (1)
    pure ()
