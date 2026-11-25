import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("x", json.string("  ")),
  ])
  let _ = my_data
}
