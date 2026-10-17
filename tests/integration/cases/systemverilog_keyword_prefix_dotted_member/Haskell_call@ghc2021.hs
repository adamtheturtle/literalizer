{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_systemverilog_keyword_prefix_dotted_member_Haskell_call where
data ThingType_ = ThingType_ { first_value :: Val -> IO () }
thing :: ThingType_
thing = ThingType_ { first_value = \_ -> return () }
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
main :: IO ()
main = do
    _ <- thing.first_value (1)
    pure ()
