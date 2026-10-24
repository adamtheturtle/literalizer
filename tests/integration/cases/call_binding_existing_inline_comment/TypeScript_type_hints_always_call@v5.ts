const make_widget: any = () => {};
const consume_widget: any = () => {};
let my_data = make_widget({ count: 42 });
consume_widget({ count: my_data });
my_data = make_widget({ count: 42 }) // note;
consume_widget({ count: my_data });
export {};
