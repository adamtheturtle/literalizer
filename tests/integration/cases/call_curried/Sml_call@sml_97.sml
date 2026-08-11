datatype val_t =
    SReal of real
  | SStr of string
  | SList of val_t list
structure throttler = struct
fun check _ _ = ()
end
val _ = throttler.check (SStr "user_1") (SReal 1000.0)
val _ = throttler.check (SStr "user_2") (SReal 2000.5)
