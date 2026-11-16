fn main() {
    fn make_widget(value: &'static std::ffi::CStr) -> &'static std::ffi::CStr { value }
    let mut my_data = c"seed";
    assert_eq!(my_data.to_bytes(), b"seed");

    my_data = make_widget(cr#"// payload;"#); assert_eq!(my_data.to_bytes(), b"// payload;");
}
