import gleam/dict

pub fn main() {
  let my_data = [
    dict.from_list([#("name", "Alice"), #("age", 30)]),
    dict.from_list([#("name", "Bob"), #("age", 25)]),
  ]
  let _ = my_data
}
