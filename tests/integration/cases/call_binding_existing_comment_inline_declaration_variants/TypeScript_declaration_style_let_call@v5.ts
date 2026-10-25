const make_widget: any = () => {};
const consume: any = () => {};
let my_data = make_widget({ count: 42 });
consume({ count: my_data });
my_data = make_widget({ count: 42 }) // note;
consume({ count: my_data });
export {};
