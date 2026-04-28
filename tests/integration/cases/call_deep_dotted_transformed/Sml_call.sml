datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
structure app = struct
structure client = struct
fun fetch _ = ()
end
end
fun emit _ = ()
val _ = emit(app.client.fetch("hello"))
val _ = emit(app.client.fetch(42))
val _ = emit(app.client.fetch(SBool true))
