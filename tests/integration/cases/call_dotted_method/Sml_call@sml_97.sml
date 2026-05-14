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
val _ = app.client.fetch("hello")
val _ = app.client.fetch(42)
val _ = app.client.fetch(SBool true)
