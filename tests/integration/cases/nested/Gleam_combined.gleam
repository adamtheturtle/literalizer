import gleam/dict

pub fn main() {
  let my_data = dict.from_list([
    #("users", [dict.from_list([#("name", "Bob"), #("tags", ["admin", "user"])]), dict.from_list([#("name", "Carol"), #("tags", ["guest"])])]),
  ])
  let my_data = dict.from_list([
    #("users", [dict.from_list([#("name", "Bob"), #("tags", ["admin", "user"])]), dict.from_list([#("name", "Carol"), #("tags", ["guest"])])]),
  ])
  let _ = my_data
}
