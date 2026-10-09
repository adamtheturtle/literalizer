import gleam/json
pub fn consume(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let my_null: json.Json = json.null()
  let regular_null: json.Json = json.null()
  consume(my_null)
  consume(regular_null)
}
