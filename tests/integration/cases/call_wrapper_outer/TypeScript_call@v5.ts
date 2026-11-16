const expectedEvents = [1, 42, 2, 142];
let eventIndex = 0;
function observeEvent(actual: number) {
    if (eventIndex >= 4 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function process({value}: { value: number }) {
    observeEvent(1); observeEvent(value);
    return value + 100;
}
function emit(actual: number) { observeEvent(2); observeEvent(actual); }
function verify_events(..._arguments: unknown[]) { if (eventIndex !== 4) throw new Error("missing receiver events"); }
emit(process({ value: 42 }));
verify_events({  });
export {};
