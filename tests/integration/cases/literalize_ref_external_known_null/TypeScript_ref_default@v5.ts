const consume_widget: any = () => {};
const item = null;
let my_data = null;
consume_widget({ arg_value: my_data });
my_data = item;
consume_widget({ arg_value: my_data });
export {};
