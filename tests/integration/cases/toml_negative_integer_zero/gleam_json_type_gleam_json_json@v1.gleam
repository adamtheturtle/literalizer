import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("value", json.float(-0.0)),
  ])
  let _ = my_data
}
