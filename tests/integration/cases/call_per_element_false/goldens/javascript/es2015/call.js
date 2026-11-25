const expectedEvents = [1, 1];
let eventIndex = 0;
function observeEvent(actual) {
    if (eventIndex >= 2 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function process({data}) {
    observeEvent(1); observeEvent(data);
    return data + 100;
}
function verify_events() { if (eventIndex !== 2) throw new Error("missing receiver events"); }
process({ data: 1 });
verify_events({  });
