const expectedEvents = [1, 1];
let eventIndex = 0;
function observeEvent(actual) {
    if (eventIndex >= 2 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function capture({__proto__}) {
    observeEvent(1); observeEvent(__proto__);
    return __proto__ + 100;
}
function verify_events() { if (eventIndex !== 2) throw new Error("missing receiver events"); }
capture({ ['__proto__']: 1 });
verify_events({  });
