import gleam/json
pub fn consume_widget(_arg_value: json.Json) -> Nil { Nil }

pub fn main() {
  let item: json.Json = json.null()
  let my_data: json.Json = json.null()
  let _ = consume_widget(my_data)
  let my_data: json.Json = item
  let _ = consume_widget(my_data)
}
