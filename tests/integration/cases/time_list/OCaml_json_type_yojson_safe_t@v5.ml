module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("times", `List [`String "09:30:00"; `String "17:45:00"; `String "23:59:59"])
]

end
