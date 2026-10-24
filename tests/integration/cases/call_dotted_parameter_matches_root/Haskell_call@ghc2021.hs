{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_dotted_parameter_matches_root_Haskell_call where
data OuterType_ = OuterType_ { inner :: Val -> Val -> IO () }
outer :: OuterType_
outer = OuterType_ { inner = \_ _ -> return () }
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
main :: IO ()
main = do
    _ <- outer.inner (1) (2)
    pure ()
