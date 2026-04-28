{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_mixed_type_dicts_Haskell_call where
data Val = HBool Bool | HStr String | HList [Val] | HMap [(String, Val)]
data MgrType_ = MgrType_ { op :: Val -> IO () }
data AppType_ = AppType_ { mgr :: MgrType_ }
app :: AppType_
app = AppType_ { mgr = MgrType_ { op = \_ -> return () } }
main :: IO ()
main = do
    _ <- app.mgr.op(HMap [("type", HStr "create"), ("pr_id", HStr "pr_1"), ("draft", HBool True)])
    _ <- app.mgr.op(HMap [("type", HStr "create"), ("pr_id", HStr "pr_2")])
    pure ()
