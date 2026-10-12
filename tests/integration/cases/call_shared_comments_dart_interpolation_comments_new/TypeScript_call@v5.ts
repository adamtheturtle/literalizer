const make_widget: any = () => {};
const my_data = ("${ /* } " block */ 42 // } " line
}").length >= 0 ? make_widget({ count: 42 }) : make_widget({ count: 42 }) // trailing
// extra;
export {};
