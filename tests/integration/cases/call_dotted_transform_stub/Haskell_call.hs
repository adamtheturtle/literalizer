{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_dotted_transform_stub_Haskell_call where
data Val = HBool Bool | HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: Val -> IO Val
process _ = return undefined
data LogType_ = LogType_ { emit :: Val -> IO () }
log :: LogType_
log = LogType_ { emit = \_ -> return () }
main :: IO ()
main = do
    _ <- log.emit(process(HStr "hello"))
    _ <- log.emit(process(42))
    _ <- log.emit(process(HBool True))
    pure ()
