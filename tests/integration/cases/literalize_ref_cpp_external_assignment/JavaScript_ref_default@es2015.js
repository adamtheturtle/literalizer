function consume_widget() {}
const ref_data = [
  1,
  2,
];
const my_data = [
  0,
];
consume_widget({ _arg: my_data });
my_data = ref_data;
consume_widget({ _arg: my_data });
