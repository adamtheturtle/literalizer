const consume_widget: any = () => {};
const ref_data = [
  1,
  2,
];
let my_data = [
  0,
];
consume_widget({ arg_value: my_data });
my_data = ref_data;
consume_widget({ arg_value: my_data });
export {};
