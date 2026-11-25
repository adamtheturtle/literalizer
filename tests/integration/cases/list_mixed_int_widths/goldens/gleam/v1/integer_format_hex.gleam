pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0x1),
    GInt(0x10000000000),
  ])
  let _ = my_data
}
