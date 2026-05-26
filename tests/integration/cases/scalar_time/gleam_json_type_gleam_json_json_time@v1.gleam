import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("starts_at", json.string("09:30:00")),
  ])
  let _ = my_data
}
