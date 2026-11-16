const expectedEvents = [1, 1, 2, 101, 3, 42];
let eventIndex = 0;
function observeEvent(actual: number) {
    if (eventIndex >= 6 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function process({value}: { value: number }) {
    observeEvent(1); observeEvent(value);
    return value + 100;
}
function emit(actual: number, zipped: number) { observeEvent(2); observeEvent(actual); observeEvent(3); observeEvent(zipped); }
function verify_events(..._arguments: unknown[]) { if (eventIndex !== 6) throw new Error("missing receiver events"); }
emit(process({ value: 1 }), 42);
verify_events({  });
export {};
