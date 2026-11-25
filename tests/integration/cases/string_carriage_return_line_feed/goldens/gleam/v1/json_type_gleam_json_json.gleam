import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("cr", json.string("a\rb")),
    #("crlf", json.string("a\r\nb")),
    #("lf", json.string("a\nb")),
  ])
  let _ = my_data
}
