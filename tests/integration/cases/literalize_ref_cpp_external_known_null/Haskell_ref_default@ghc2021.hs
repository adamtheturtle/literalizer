module Fixture_literalize_ref_cpp_external_known_null_Haskell_ref_default where
data Val = HNull | HList [Val]
consume_widget :: a -> IO ()
consume_widget _ = return ()
item :: Val
item = HNull
my_data :: Val
my_data = HNull
consume_widget my_data
my_data = item
main :: IO ()
main = do
    _ <- consume_widget my_data
    pure ()
