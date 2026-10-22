module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("cr", `String "a\rb");
    ("crlf", `String "a\r\nb");
    ("lf", `String "a\nb")
]

end
