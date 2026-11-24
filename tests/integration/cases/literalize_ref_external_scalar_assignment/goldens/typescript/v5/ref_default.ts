const consume_widget: any = () => {};
let my_data = 0;
const shared = 1;
consume_widget({ arg_value: my_data });
my_data = shared;
consume_widget({ arg_value: my_data });
export {};
