module Fixture_json5_comment_empty_list_Haskell where
data Val = HList [Val]
-- empty heading
-- empty body
-- after empty
my_data :: Val
my_data = HList []
main :: IO ()
main = seq my_data (return ())
