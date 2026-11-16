const expectedEvents = [1, 42];
let eventIndex = 0;
function observeEvent(actual: number) {
    if (eventIndex >= 2 || actual !== expectedEvents[eventIndex]) throw new Error("receiver event changed");
    eventIndex++;
}
function f({a}: { a: number }) {
    observeEvent(1); observeEvent(a);
    return a + 100;
}
function verify_events(..._arguments: unknown[]) { if (eventIndex !== 2) throw new Error("missing receiver events"); }
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f({ a: 42 });
verify_events({  });
export {};
