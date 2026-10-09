module Fixture_call_ref_cpp_string_ownership_Haskell_call where
data Val = HStr String | HList [Val]
consume :: Val -> IO ()
consume _ = return ()
item :: Val
item = HStr "s"
main :: IO ()
main = do
    _ <- consume item
    pure ()
