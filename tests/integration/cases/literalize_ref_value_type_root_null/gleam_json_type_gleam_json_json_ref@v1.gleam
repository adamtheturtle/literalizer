import gleam/json

pub fn main() {
  let shared: json.Json = json.null()
  let my_data: json.Json = shared
  let _ = my_data
}
