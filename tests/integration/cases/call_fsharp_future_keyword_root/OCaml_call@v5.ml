module Check = struct

module Process = struct
module Api = struct
let fetch _ = ()
end
end
type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let _ = Process.Api.fetch(OMap [("data", OStr "hello")])
let _ = Process.Api.fetch(OMap [("data", OInt 42)])
let _ = Process.Api.fetch(OMap [("data", OBool true)])

end
