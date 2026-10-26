module Fixture_literalize_ref_external_repeated_opaque_list_Haskell_ref_default where
data Val = HList [Val]
consume_widget :: Val -> IO ()
consume_widget _ = return ()
item :: Val
item = HList []
my_data :: Val
my_data = HList [
    item,
    item
    ]
main :: IO ()
main = do
    _ <- consume_widget my_data
    pure ()
