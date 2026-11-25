module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("within_i32", `String "2024-01-15T12:00:00");
    ("beyond_i32", `String "2099-06-15T08:30:00")
]

end
