module Fixture_call_no_params_Haskell_call where
data Val = HList [Val]
process :: IO ()
process = return ()
main :: IO ()
main = do
    _ <- process
    _ <- process
    pure ()
