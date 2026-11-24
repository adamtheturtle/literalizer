datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
structure my_app = struct
structure http_client = struct
fun fetch _ = ()
end
end
val _ = my_app.http_client.fetch(SStr "hello")
val _ = my_app.http_client.fetch(SInt 42)
val _ = my_app.http_client.fetch(SBool true)
