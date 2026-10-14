pub type GVal {
  GList(List(GVal))
}
pub fn process() -> Nil { Nil }
pub fn emit(__arg: a) -> Nil { Nil }

pub fn main() {
  let _ = emit(process())
  let _ = emit(process())
}
