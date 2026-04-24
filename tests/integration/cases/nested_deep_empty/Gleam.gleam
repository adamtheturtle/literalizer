pub type GVal {
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GList([]), GList([])]),
  ])
  let _ = my_data
}
