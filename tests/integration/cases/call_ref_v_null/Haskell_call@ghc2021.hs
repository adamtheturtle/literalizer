module Fixture_call_ref_v_null_Haskell_call where
data Val = HNull
consume :: Val -> IO ()
consume _ = return ()
value :: Val
value = HNull
main :: IO ()
main = do
    _ <- consume value
    pure ()
