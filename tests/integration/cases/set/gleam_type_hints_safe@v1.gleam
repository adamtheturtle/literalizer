pub type GVal {
  GStr(String)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GStr("apple"),
    GStr("banana"),
    GStr("cherry"),
  ])
  let _ = my_data
}
