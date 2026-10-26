datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
structure api = struct
structure worker = struct
fun process _ = ()
end
end
val _ = api.worker.process(SList [SInt 1, SMap []], SInt 42)
val _ = api.worker.process(SList [SInt 2, SMap [("x", SStr "s")]], SInt 43)
