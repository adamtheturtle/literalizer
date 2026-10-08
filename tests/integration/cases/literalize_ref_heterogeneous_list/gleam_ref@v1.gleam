pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let one = GInt(1)
  let two = GStr("s")
  let my_data = GList([
    one,
    two,
  ])
  let _ = my_data
}
