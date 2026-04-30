module Fixture_call_no_params_transform_Haskell_call where
data Val = HList [Val]
process :: () -> IO Val
process _ = return undefined
emit :: a -> IO ()
emit _ = return ()
main :: IO ()
main = do
    _ <- emit(process())
    _ <- emit(process())
    pure ()
