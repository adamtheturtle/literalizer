const expectedEvents = [1, 1, 2, 101, 3, 42];
let eventIndex = 0;
function observeEvent(actual) {
    if (eventIndex >= 6 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function process({value}) {
    observeEvent(1); observeEvent(value);
    return value + 100;
}
function emit(actual, zipped) { observeEvent(2); observeEvent(actual); observeEvent(3); observeEvent(zipped); }
function verify_events() { if (eventIndex !== 6) throw new Error("missing receiver events"); }
emit(process({ value: 1 }), 42);
verify_events({  });
