{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_dotted_receiver_parameter_collisions_Haskell_call where
data WorkerType_ = WorkerType_ { process :: Val -> Val -> IO () }
data ApiType_ = ApiType_ { worker :: WorkerType_ }
api :: ApiType_
api = ApiType_ { worker = WorkerType_ { process = \_ _ -> return () } }
data Val = HStr String | HList [Val] | HMap [(String, Val)]
main :: IO ()
main = do
    _ <- api.worker.process (HMap []) (HMap [])
    pure ()
