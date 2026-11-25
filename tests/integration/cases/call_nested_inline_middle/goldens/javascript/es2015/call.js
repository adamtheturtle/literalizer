function f() {}
f({ ops: [["DEL", "b", "10"], ["ADD", "a", "x"]] });  // note
// next call
f({ ops: [["ADD", "c", "y"]] });
