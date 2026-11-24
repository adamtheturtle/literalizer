import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("a", json.object([])),
    #("b", json.int(1)),
  ])
  let _ = my_data
}
