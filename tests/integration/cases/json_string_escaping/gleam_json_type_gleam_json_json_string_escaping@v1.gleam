import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("$key", json.string("a\"b\tcé #{world} $ident")),
  ])
  let _ = my_data
}
