import gleam/json

pub fn main() {
  let my_data: json.Json = json.string("2024-01-15T18:00:00+05:00")
  let _ = my_data
}
