pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("custom base after empty collision: )\"\nvalue"),
    GStr("custom suffix after base collision: )\" and )x0\"\nvalue"),
    GStr("custom second suffix: )\" and )x0\" and )x00\"\nvalue"),
    GStr("long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"),
  ])
  let _ = my_data
}
