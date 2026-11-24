pub type GVal {
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    // outer heading
    // first empty
    GList([]),
    // second empty
    GList([]),
  ])
  let _ = my_data
  let my_data = GList([
    // outer heading
    // first empty
    GList([]),
    // second empty
    GList([]),
  ])
  let _ = my_data
}
