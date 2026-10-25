pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
      let shared = GList([
        GInt(1),
        GInt(2),
      ])
      let my_data = GList([
        // A leading comment with { braces, "quotes", and // markers
        GStr("first\n{ \"quoted\" // text }"),
        shared,
      ])
  let _ = my_data
}
