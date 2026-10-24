datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
structure foo = struct
fun class _ = ()
end
val _ = foo.class(SInt 1)
