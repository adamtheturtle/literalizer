const expectedEvents = [1, 42, 1, 42, 1, 142];
let eventIndex = 0;
function observeEvent(actual: number) {
    if (eventIndex >= 6 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function make_widget({count}: { count: number }) {
    observeEvent(1); observeEvent(count);
    return count + 100;
}
function verify_events(..._arguments: unknown[]) { if (eventIndex !== 6) throw new Error("missing receiver events"); }
let my_data: number = 42;
make_widget({ count: my_data });
my_data = make_widget({ count: my_data });
make_widget({ count: my_data });
verify_events({  });
export {};
