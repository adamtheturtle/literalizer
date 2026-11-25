import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("date", json.string("2024-01-15")),
    #("datetime", json.string("2024-01-15T12:30:00+00:00")),
  ])
  let _ = my_data
}
