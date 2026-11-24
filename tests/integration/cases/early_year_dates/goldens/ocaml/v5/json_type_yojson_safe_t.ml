module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("date", `String "0099-05-27");
    ("naive", `String "0001-01-01T12:30:00");
    ("recent", `String "2024-05-27T10:00:00")
]

end
