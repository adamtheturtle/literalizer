import gleam/dict

pub fn main() {
  let my_data = [
    dict.from_list([#("first", "Alice"), #("last", "Smith"), #("middle", "Jane")]),
    dict.from_list([#("first", "Bob"), #("last", "Jones")]),
  ]
  let my_data = [
    dict.from_list([#("first", "Alice"), #("last", "Smith"), #("middle", "Jane")]),
    dict.from_list([#("first", "Bob"), #("last", "Jones")]),
  ]
  let _ = my_data
}
