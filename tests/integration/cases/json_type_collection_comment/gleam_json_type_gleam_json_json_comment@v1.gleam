import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("a", json.int(1)),  // About a.
    #("b", json.int(2)),
  ])
  let _ = my_data
}
