import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("name", json.string("Alice")),
    #("age", json.int(30)),
    #("active", json.bool(True)),
  ])
  let _ = my_data
}
