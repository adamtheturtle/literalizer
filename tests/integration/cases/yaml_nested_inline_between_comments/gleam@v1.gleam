pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(2), GStr("hello")]),  // trailing note
    // next element
    GList([GInt(3), GStr("world")]),
  ])
  let _ = my_data
}
