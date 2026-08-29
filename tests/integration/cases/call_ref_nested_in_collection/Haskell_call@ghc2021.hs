module Fixture_call_ref_nested_in_collection_Haskell_call where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
process :: Val -> Val -> IO ()
process _ _ = return ()
big_list :: Val
big_list = HList [
    HStr "x"
    ]
main :: IO ()
main = do
    _ <- process (HMap [("k", big_list)]) (HMap [("m", big_list)])
    pure ()
