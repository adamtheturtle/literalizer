pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GStr("Dune"))  // first edition
  let _ = process(GStr("Solaris"))
  let _ = process(GStr("Neuromancer"))  // cyberpunk
}
