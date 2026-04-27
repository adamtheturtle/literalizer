structure Check = struct

datatype val_t =
    SReal of real
  | SStr of string
  | SList of val_t list
structure throttler = struct
fun check _ = ()
end
fun emit _ = ()
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))

end
