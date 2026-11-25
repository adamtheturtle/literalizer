const expectedEvents = [1, -1, 1, -2, 1, -3];
let eventIndex = 0;
function observeEvent(actual: number) {
    if (eventIndex >= 6 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function process({value}: { value: number }) {
    observeEvent(1); observeEvent(value);
    return value + 100;
}
function verify_events(..._arguments: unknown[]) { if (eventIndex !== 6) throw new Error("missing receiver events"); }
process({ value: -1 });
process({ value: -2 });
process({ value: -3 });
verify_events({  });
export {};
