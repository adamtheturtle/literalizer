pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    // strings stay data
    GStr("https://example.org/a/*b*/"),  // URL annotation
    GStr("escaped quote: \" // still data"),
    GStr("backslash: \\"),  // outside the string
    GStr("/* not a comment */"),
  ])
  let _ = my_data
  let my_data = GList([
    // strings stay data
    GStr("https://example.org/a/*b*/"),  // URL annotation
    GStr("escaped quote: \" // still data"),
    GStr("backslash: \\"),  // outside the string
    GStr("/* not a comment */"),
  ])
  let _ = my_data
}
