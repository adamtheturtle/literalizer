pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0xde0b6b3a763ffff),
    GInt(-{0xde0b6b3a763ffff}),
  ])
  let _ = my_data
}
