import gleam/json
pub fn consume_widget(_arg_value: json.Json) -> Nil { Nil }

pub fn main() {
  let shared: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let my_data: json.Json = shared
  let _ = consume_widget(my_data)
}
