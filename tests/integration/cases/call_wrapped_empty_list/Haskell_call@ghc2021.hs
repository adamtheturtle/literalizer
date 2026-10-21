module Fixture_call_wrapped_empty_list_Haskell_call where
make_widget :: Val -> IO ()
make_widget _ = return ()
data Val = HList [Val]
main :: IO ()
main = do
    _ <- make_widget (HList [])
    pure ()
