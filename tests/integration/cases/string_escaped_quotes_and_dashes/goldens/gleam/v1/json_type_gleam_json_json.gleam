import gleam/json

pub fn main() {
  let my_data: json.Json = json.string("hello \"world\" -- not a comment")
  let _ = my_data
}
