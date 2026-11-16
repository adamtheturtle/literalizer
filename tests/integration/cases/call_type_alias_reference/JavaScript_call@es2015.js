const expectedEvents = [1, 1];
let eventIndex = 0;
function observeEvent(actual) {
    if (eventIndex >= 2 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function process({value}) {
    observeEvent(1); observeEvent(value);
    return value + 100;
}
function verify_events() { if (eventIndex !== 2) throw new Error("missing receiver events"); }
const value = 1;
process({ value: value });
verify_events({  });
