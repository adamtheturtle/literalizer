import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("a", json.int(9223372036854775807)),
    #("b", json.int(9223372036854775808)),
  ])
  let _ = my_data
}
