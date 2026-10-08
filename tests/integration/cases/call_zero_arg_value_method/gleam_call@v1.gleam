pub type GVal {
  GList(List(GVal))
}
pub fn thing_go() -> Nil { Nil }

pub fn main() {
  thing_go()
}
