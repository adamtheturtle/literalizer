const make_widget: any = () => {};
const consume: any = () => {};
const my_data = make_widget({ first: 42, second: 3 });
consume({ first: my_data, second: 3 });
export {};
