import gleam/json
pub fn make_widget(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let my_data: json.Json = make_widget(json.preprocessed_array([]))
  let _ = my_data
}
