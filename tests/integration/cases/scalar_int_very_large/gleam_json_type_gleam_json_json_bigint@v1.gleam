import gleam/json

pub fn main() {
  let my_data: json.Json = json.int(9223372036854775808)
  let _ = my_data
}
