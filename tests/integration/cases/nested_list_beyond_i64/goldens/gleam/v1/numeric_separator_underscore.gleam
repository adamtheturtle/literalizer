pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(1)]),
    GList([GInt(1_180_591_620_717_411_303_424)]),
  ])
  let _ = my_data
}
