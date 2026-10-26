const make_widget: any = () => {};
const consume: any = () => {};
let my_data = make_widget({ value: 42 });
consume({ value: my_data });
my_data = make_widget({ value: 42 });
consume({ value: my_data });
export {};
