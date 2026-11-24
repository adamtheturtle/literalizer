module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("exact_millisecond", `String "09:30:15.123000");
    ("sub_millisecond", `String "09:30:15.123456")
]

end
