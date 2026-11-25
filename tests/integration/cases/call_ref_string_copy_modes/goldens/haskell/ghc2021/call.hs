module Fixture_call_ref_string_copy_modes_Haskell_call where
data Val = HStr String | HList [Val]
consume :: Val -> IO ()
consume _ = return ()
item :: Val
item = HStr "s"
main :: IO ()
main = do
    _ <- consume item
    pure ()
