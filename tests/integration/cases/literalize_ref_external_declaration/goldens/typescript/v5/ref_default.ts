const consume_widget: any = () => {};
const shared = [
  1,
  2,
];
const my_data = shared;
consume_widget({ arg_value: my_data });
export {};
