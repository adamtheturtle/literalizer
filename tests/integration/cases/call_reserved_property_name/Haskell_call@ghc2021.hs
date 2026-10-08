{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_reserved_property_name_Haskell_call where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
data FooType_ = FooType_ { class :: Val -> IO () }
foo :: FooType_
foo = FooType_ { class = \_ -> return () }
main :: IO ()
main = do
    _ <- foo.class (1)
    pure ()
