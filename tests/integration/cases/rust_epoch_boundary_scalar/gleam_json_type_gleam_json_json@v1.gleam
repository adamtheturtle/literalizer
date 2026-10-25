import gleam/json

pub fn main() {
  let my_data: json.Json = json.string("2099-06-15T08:30:00")
  let _ = my_data
}
