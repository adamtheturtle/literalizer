module Fixture_call_unknown_ref_values_nested_list_Haskell_call where
data Val = HList [Val]
process :: Val -> IO ()
process _ = return ()
unknown_value :: Val
unknown_value = HList []
main :: IO ()
main = do
    _ <- process (HList [unknown_value])
    pure ()
