function process() {}
const known_value = true;
const unknown_value = true;
process({ known_value: known_value, nested_missing: [unknown_value] });
