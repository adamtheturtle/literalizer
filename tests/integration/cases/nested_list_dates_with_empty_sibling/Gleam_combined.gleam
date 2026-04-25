pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GStr("2026-01-01"), GStr("2026-01-02")]),
    GList([]),
    GList([GStr("2026-02-03"), GStr("2026-02-04")]),
  ])
  let my_data = GList([
    GList([GStr("2026-01-01"), GStr("2026-01-02")]),
    GList([]),
    GList([GStr("2026-02-03"), GStr("2026-02-04")]),
  ])
  let _ = my_data
}
