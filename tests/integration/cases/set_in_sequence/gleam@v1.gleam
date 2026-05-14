pub type GVal {
  GStr(String)
  GList(List(GVal))
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GSet([GStr("a"), GStr("b")]),
  ])
  let _ = my_data
}
