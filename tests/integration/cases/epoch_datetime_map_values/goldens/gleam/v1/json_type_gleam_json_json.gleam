import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("within_i32", json.string("2024-01-15T12:00:00")),
    #("beyond_i32", json.string("2099-06-15T08:30:00")),
  ])
  let _ = my_data
}
