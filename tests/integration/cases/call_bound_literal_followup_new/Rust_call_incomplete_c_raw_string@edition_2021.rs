fn main() {
    fn make_widget(value: &'static std::ffi::CStr) -> &'static std::ffi::CStr { value }
    let my_data = make_widget(cr#"// payload;"#); assert_eq!(my_data.to_bytes(), b"// payload;");
}
