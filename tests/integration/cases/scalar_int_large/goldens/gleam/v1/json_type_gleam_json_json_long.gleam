import gleam/json

pub fn main() {
  let my_data: json.Json = json.int(2147483648)
  let _ = my_data
}
