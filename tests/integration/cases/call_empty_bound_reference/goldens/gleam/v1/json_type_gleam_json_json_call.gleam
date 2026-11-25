import gleam/json
pub fn make_widget(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let items: json.Json = json.preprocessed_array([])
  let _ = make_widget(items)
}
