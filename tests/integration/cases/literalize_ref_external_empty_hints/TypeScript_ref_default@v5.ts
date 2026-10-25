const consume_widget: any = () => {};
const item = [
  1,
  2,
];
let my_data = [
  1,
  2,
];
consume_widget({ arg_value: my_data });
my_data = item;
consume_widget({ arg_value: my_data });
export {};
