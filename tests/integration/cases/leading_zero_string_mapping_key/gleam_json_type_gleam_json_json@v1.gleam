import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("08", json.string("value")),
  ])
  let _ = my_data
}
