import gleam/dict
pub fn main() {
  let my_data = [
    dict.from_list([#("type", "create"), #("pr_id", "pr_1"), #("draft", True)]),
    dict.from_list([#("type", "create"), #("pr_id", "pr_2")]),
  ]
  let my_data = [
    dict.from_list([#("type", "create"), #("pr_id", "pr_1"), #("draft", True)]),
    dict.from_list([#("type", "create"), #("pr_id", "pr_2")]),
  ]
  let _ = my_data
}
