pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0o1),
    GInt(0o20000000000000),
  ])
  let _ = my_data
}
