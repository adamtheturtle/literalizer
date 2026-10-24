import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("v", json.string("a‪\u{0000}é😀b")),
  ])
  let _ = my_data
}
