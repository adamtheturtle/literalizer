import gleam/json
pub fn consume_widget(_arg_value: json.Json) -> Nil { Nil }

pub fn main() {
  let my_data: json.Json = json.object([
    #("a", json.int(0)),
  ])
  let _ = consume_widget(my_data)
  let my_data: json.Json = json.object([
    #("a", json.int(1)),
  ])
  let _ = consume_widget(my_data)
}
