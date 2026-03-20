fn main() {
    {
        let my_data = "hello \"world\" -- not a comment";
        let _ = my_data;
    }
    let my_data;
    my_data = "hello \"world\" -- not a comment";
    let _ = my_data;
}
