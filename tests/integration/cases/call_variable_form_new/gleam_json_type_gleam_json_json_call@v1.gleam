import gleam/json
pub fn make_widget(_count: json.Json) -> Nil { Nil }

pub fn main() {
  let my_data: json.Json = make_widget(json.int(42))
  let _ = my_data
}
