import gleam/json

pub fn main() {
  let my_data: json.Json = json.string("\nroot first line\n  indented\n\nroot last line\n")
  let _ = my_data
}
