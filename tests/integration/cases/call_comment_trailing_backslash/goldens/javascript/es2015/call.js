const expectedEvents = [1, 1, 1, 2];
let eventIndex = 0;
function observeEvent(actual) {
    if (eventIndex >= 4 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function process({value}) {
    observeEvent(1); observeEvent(value);
    return value + 100;
}
function verify_events() { if (eventIndex !== 4) throw new Error("missing receiver events"); }
process({ value: 1 });  // trail \ .
process({ value: 2 });  // second
verify_events({  });
