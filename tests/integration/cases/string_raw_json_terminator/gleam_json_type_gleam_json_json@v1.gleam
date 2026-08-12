import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #(")json", json.string("x")),
  ])
  let _ = my_data
}
