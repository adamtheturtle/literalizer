import gleam/set

pub fn main() {
  let my_data = set.from_list([
    "apple",  // inline comment
    // before banana
    "banana",
    // trailing
  ])
  let _ = my_data
}
