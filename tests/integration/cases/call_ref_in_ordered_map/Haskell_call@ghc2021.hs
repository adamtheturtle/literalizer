module Fixture_call_ref_in_ordered_map_Haskell_call where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
process :: Val -> IO ()
process _ = return ()
big_list :: Val
big_list = HList [
    HStr "x"
    ]
main :: IO ()
main = do
    _ <- process (HMap [("m", big_list)])
    pure ()
