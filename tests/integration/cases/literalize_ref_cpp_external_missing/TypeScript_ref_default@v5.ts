const consume_widget: any = () => {};
const item = [
  1,
  2,
];
const my_data = [
  1,
  2,
];
consume_widget({ _arg: my_data });
my_data = item;
consume_widget({ _arg: my_data });
export {};
