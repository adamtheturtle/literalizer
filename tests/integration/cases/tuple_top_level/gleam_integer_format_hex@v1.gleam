pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0x1),
    GStr("email"),
    GStr("a@gmail.com"),
    GInt(0x64),
  ])
  let _ = my_data
}
