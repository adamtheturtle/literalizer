datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
structure tracer = struct
fun emit _ = ()
end
val _ = tracer.emit(process(SStr "hello"))
val _ = tracer.emit(process(SInt 42))
val _ = tracer.emit(process(SBool true))
