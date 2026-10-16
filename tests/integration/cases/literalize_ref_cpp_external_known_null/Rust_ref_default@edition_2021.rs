fn main() {
    let item = None::<()>;
    let my_data = None::<()>;
    (void)my_data;
    my_data = item;
    (void)my_data;
}
