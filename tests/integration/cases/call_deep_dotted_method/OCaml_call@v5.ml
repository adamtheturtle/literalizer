module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
module Obj = struct
module Api = struct
module Client = struct
let post _ = ()
end
end
end
let _ = Obj.Api.Client.post("hello")
let _ = Obj.Api.Client.post(42)
let _ = Obj.Api.Client.post(OBool true)

end
