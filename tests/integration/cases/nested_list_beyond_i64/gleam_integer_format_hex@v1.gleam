pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(0x1)]),
    GList([GInt(0x400000000000000000)]),
  ])
  let _ = my_data
}
