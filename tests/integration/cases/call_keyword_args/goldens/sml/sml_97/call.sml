datatype val_t =
    SReal of real
  | SStr of string
  | SList of val_t list
structure throttler = struct
fun check _ = ()
end
fun emit _ = ()
val _ = emit(throttler.check(SStr "user_1", SReal 1000.0))
val _ = emit(throttler.check(SStr "user_2", SReal 2000.5))
