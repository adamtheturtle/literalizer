fn main() {
    static MY_INT: i32 = 42;
    static MY_DATA: i32 = MY_INT;
    let _ = &MY_DATA;
}
