structure outer = struct
fun inner _ = ()
end
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = outer.inner(SInt 1, SInt 2)
