datatype val_t =
    SStr of string
  | SList of val_t list
structure app = struct
structure client = struct
fun fetch _ = ()
end
end
val _ = app.client.fetch(SStr "hello")
val _ = app.client.fetch(SStr "world")
