module Fixture_call_nim_empty_statement_Haskell_call where
make_widget :: Val -> IO ()
make_widget _ = return ()
data Val = HList [Val]
main :: IO ()
main = do
    _ <- make_widget (HList [])
    pure ()
