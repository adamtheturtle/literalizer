import gleam/dict
pub fn main() {
  let my_data = dict.from_list([
    #("1", "one"),
    #("2", "two"),
    #("42", "answer"),
  ])
  let _ = my_data
}
