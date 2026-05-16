pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  process(GStr("Dune"))  // first edition
  process(GStr("Solaris"))
  process(GStr("Neuromancer"))  // cyberpunk
}
