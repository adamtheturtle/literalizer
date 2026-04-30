const process: any = () => {};
const my_var = 42;
const my_other = 7;
process({ data: [{"ref": "my_var"}, 42, "static"] });
process({ data: [{"ref": "my_other"}, 7, "label"] });
export {};
