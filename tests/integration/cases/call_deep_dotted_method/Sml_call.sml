structure Check = struct

datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
structure obj = struct
structure api = struct
structure client = struct
fun post _ = ()
end
end
end
val _ = obj.api.client.post("hello")
val _ = obj.api.client.post(42)
val _ = obj.api.client.post(SBool true)

end
