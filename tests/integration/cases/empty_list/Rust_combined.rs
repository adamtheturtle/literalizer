fn main() {
    {
        let my_data = Vec::<String>::new();
        let _ = my_data;
    }
    let my_data;
    my_data = Vec::<String>::new();
    let _ = my_data;
}
