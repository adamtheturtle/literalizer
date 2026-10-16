const make_widget: any = () => {};
let my_data = make_widget({ count: 42 });
make_widget({ count: my_data });
my_data = make_widget({ count: my_data }) // note;
make_widget({ count: my_data });
export {};
