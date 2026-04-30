fn main() {
    fn process<A, B, C>(_ts: A, _start: B, _end: C) {}
    process(1, 0, 3600);  // Jan 1 1970 00:00:00 - 01:00:00
    process(5, 0, 3600);  // Jan 1 1970 00:00:05 - 01:00:05
    process(2, 0, 5400);  // Jan 1 1970 00:00:02 - 01:30:02
}
