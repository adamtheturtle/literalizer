const expectedEvents = [1, 42, 2, 142];
let eventIndex = 0;
function observeEvent(actual: number) {
    if (eventIndex >= 4 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function make_widget({value}: { value: number }) {
    observeEvent(1); observeEvent(value);
    return value + 100;
}
function consume({value}: { value: number }) { observeEvent(2); observeEvent(value); }
function verify_events(..._arguments: unknown[]) { if (eventIndex !== 4) throw new Error("missing receiver events"); }
const my_data = make_widget({ value: 42 });
consume({ value: my_data });
verify_events({  });
export {};
