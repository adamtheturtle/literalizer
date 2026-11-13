export {};

let calls = 0, checks = 0;
function ensure(value: boolean): void { if (!value) throw new Error("checked call changed"); }
const counter = {accept(user: string, timestamp: number): boolean {
    ensure(user === (calls === 0 ? "user_1" : "user_2"));
    ensure(timestamp === 100.0 + calls);
    calls++;
    return user === "user_1";
}};
function checkResult(actual: boolean, expected: (boolean | string)[]): void {
    ensure(actual === expected[0]);
    ensure(expected[1] === (checks === 0 ? "first" : "second"));
    checks++;
}
function run(): void {
  checkResult(counter.accept("user_1", 100.0), [true, "first"]);
}
run();
ensure(calls === 1 && checks === 1);
