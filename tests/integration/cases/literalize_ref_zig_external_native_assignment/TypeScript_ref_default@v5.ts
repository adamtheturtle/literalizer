const consume_widget: any = () => {};
const shared = [
  1,
  2,
];
var my_data = [
  0,
];
consume_widget({ _arg: my_data });
my_data = shared;
consume_widget({ _arg: my_data });
export {};
