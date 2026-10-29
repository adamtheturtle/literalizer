import gleam/json

pub fn main() {
  let my_data: json.Json = json.string("1901-12-13T20:45:51")
  let _ = my_data
}
