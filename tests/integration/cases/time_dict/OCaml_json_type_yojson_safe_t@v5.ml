module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("morning", `String "09:30:00");
    ("afternoon", `String "14:15:00");
    ("evening", `String "23:59:59")
]

end
