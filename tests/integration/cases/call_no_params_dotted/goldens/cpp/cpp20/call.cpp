struct throttlerType_ { void check(auto...) const {} };
const throttlerType_ throttler;
int main() {
throttler.check();
throttler.check();
    return 0;
}
