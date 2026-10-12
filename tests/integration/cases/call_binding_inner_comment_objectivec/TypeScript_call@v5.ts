const make_widget: any = () => {};
const my_data = make_widget({ count: 42 }) ?
make_widget({ count: 42 }) // inner
: nil // trailing;
export {};
