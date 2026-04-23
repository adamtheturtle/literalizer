{-# LANGUAGE OverloadedRecordDot #-}
module Check where
data Val = HBool Bool | HStr String | HList [Val] | HMap [(String, Val)]
data MgrType_ = MgrType_ { Op :: Val -> IO () }
mgr = MgrType_ { Op = \_ -> return () }
main :: IO ()
main = do
    mgr.Op(HMap [("type", HStr "create"), ("pr_id", HStr "pr_1"), ("draft", HBool True)])
    mgr.Op(HMap [("type", HStr "create"), ("pr_id", HStr "pr_2")])
    pure ()
