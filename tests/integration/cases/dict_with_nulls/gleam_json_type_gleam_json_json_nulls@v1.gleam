import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("name", json.string("Alice")),
    #("score", json.null()),
    #("age", json.int(30)),
  ])
  let _ = my_data
}
