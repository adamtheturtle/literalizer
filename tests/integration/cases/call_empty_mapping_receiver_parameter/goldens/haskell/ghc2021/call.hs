{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_empty_mapping_receiver_parameter_Haskell_call where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
data ApiType_ = ApiType_ { process :: Val -> IO () }
api :: ApiType_
api = ApiType_ { process = \_ -> return () }
main :: IO ()
main = do
    _ <- api.process (HMap [])
    pure ()
