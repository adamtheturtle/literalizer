structure process = struct
structure api = struct
fun fetch _ = ()
end
end
datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val _ = process.api.fetch(SMap [("data", SStr "hello")])
val _ = process.api.fetch(SMap [("data", SInt 42)])
val _ = process.api.fetch(SMap [("data", SBool true)])
