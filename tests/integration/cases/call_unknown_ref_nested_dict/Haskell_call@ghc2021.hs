module Fixture_call_unknown_ref_nested_dict_Haskell_call where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
process :: Val -> IO ()
process _ = return ()
my_list :: Val
my_list = HList []
main :: IO ()
main = do
    _ <- process (HList [HList [HMap [("inner", my_list)]]])
    pure ()
