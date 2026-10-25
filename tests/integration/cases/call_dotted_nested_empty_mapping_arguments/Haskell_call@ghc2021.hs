{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_dotted_nested_empty_mapping_arguments_Haskell_call where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
data WorkerType_ = WorkerType_ { process :: Val -> Val -> IO () }
data ApiType_ = ApiType_ { worker :: WorkerType_ }
api :: ApiType_
api = ApiType_ { worker = WorkerType_ { process = \_ _ -> return () } }
main :: IO ()
main = do
    _ <- api.worker.process (HList [1, HMap []]) (42)
    _ <- api.worker.process (HList [2, HMap [("x", HStr "s")]]) (43)
    pure ()
