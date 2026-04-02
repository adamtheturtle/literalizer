import gleam/dict
pub fn main() {
  let my_data = dict.from_list([
    #("level1", dict.from_list([#("level2", dict.from_list([#("level3", dict.from_list([#("level4", dict.from_list([#("value", "deep"), #("items", ["a", "b"])]))])), #("sibling", 42)])), #("tags", [dict.from_list([#("name", "tag1"), #("meta", dict.from_list([#("priority", 1), #("labels", ["x", "y"])]))])])])),
  ])
  let _ = my_data
}
