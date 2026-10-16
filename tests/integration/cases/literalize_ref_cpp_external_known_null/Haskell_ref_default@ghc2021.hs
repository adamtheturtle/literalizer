module Fixture_literalize_ref_cpp_external_known_null_Haskell_ref_default where
data Val = HNull
item :: Val
item = HNull
my_data :: Val
my_data = HNull
main :: IO ()
main = do
    _ <- (void)my_data;
    _ <- my_data = item
    _ <- (void)my_data;
    pure ()
