structure api = struct
structure worker = struct
fun process _ = ()
end
end
datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val _ = api.worker.process(SMap [], SMap [])
