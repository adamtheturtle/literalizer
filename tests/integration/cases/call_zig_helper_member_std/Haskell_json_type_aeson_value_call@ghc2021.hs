{-# LANGUAGE QuasiQuotes #-}
{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_zig_helper_member_std_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
data ObjType_ = ObjType_ { std :: Value -> IO () }
obj :: ObjType_
obj = ObjType_ { std = \_ -> return () }
main :: IO ()
main = do
    _ <- obj.std [aesonQQ| 1 |]
    pure ()
