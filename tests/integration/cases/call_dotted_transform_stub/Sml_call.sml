datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
structure log = struct
fun emit _ = ()
end
val _ = log.emit(process("hello"))
val _ = log.emit(process(42))
val _ = log.emit(process(SBool true))
