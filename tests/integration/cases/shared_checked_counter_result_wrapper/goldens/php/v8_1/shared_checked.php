<?php
class Counter {
    public int $calls = 0;
    public function accept(string $user, float $timestamp): bool {
        if ($user !== ($this->calls === 0 ? "user_1" : "user_2") || $timestamp !== 100.0 + $this->calls) {
            throw new Exception("receiver arguments changed");
        }
        $this->calls++;
        return $user === "user_1";
    }
}
$checks = 0;
function checkResult(bool $actual, array $expected): void {
    global $checks;
    if ($actual !== $expected[0] || $expected[1] !== ($checks === 0 ? "first" : "second")) {
        throw new Exception("paired result changed");
    }
    $checks++;
}
$counter = new Counter();
checkResult($counter->accept("user_1", 100.0), [true, "first"]);
if ($counter->calls !== 1 || $checks !== 1) { throw new Exception("calls skipped"); }
