const make_widget: any = () => {};
const my_data: number = 42;
my_data = make_widget({ count: my_data })
// note;
make_widget({ count: my_data });
export {};
