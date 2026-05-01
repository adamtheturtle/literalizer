pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GStr("ADD"), GStr("alice"), GStr("hello")]),
    GList([GStr("DEL"), GStr("bob"), GStr("5")]),  // removes "world"
  ])
  let my_data = GList([
    GList([GStr("ADD"), GStr("alice"), GStr("hello")]),
    GList([GStr("DEL"), GStr("bob"), GStr("5")]),  // removes "world"
  ])
  let _ = my_data
}
