pub type GVal {
  GStr(String)
}

pub fn main() {
  let my_data = GStr("\nroot first line\n  indented\n\nroot last line\n")
  let _ = my_data
}
