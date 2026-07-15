import gleam/json

pub fn main() {
  let my_data: json.Json = json.int(-2147483649)
  let _ = my_data
}
