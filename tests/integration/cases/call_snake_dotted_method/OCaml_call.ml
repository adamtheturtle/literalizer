module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
module My_app = struct
module Http_client = struct
let fetch _ = ()
end
end
let _ = My_app.Http_client.fetch("hello")
let _ = My_app.Http_client.fetch(42)
let _ = My_app.Http_client.fetch(OBool true)

end
