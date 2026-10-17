import gleam/json
pub fn make_widget(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let value: json.Json = json.int(1)
  let _ = make_widget(value)
}
