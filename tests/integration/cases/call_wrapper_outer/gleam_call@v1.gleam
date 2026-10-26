pub type GVal {
  GInt(Int)
}
pub fn process(_value: a) -> Nil { Nil }
pub fn emit(_argument0: a) -> Nil { Nil }

pub fn main() {
  let _ = emit(process(GInt(42)))
}
