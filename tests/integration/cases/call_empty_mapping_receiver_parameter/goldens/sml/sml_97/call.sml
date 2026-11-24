datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
structure api = struct
fun process _ = ()
end
val _ = api.process(SMap [])
