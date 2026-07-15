import gleam/json

pub fn main() {
  let my_data: json.Json = json.string("a\"b\tcé")
  let _ = my_data
}
