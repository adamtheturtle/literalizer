module Fixture_call_ref_cpp_external_known_null_Haskell_call where
data Val = HNull
consume :: Val -> IO ()
consume _ = return ()
item :: Val
item = HNull
main :: IO ()
main = do
    _ <- consume item
    pure ()
