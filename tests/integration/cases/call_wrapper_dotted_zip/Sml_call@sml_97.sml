fun process _ = ()
structure helpers = struct
fun emit _ = ()
end
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = helpers.emit(process(SInt 1), SInt 42)
