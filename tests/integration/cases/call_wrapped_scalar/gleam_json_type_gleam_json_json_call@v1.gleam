import gleam/json
pub fn make_widget(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let _ = make_widget(json.int(1))
}
