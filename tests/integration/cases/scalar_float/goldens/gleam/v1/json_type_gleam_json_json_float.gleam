import gleam/json

pub fn main() {
  let my_data: json.Json = json.float(3.14)
  let _ = my_data
}
