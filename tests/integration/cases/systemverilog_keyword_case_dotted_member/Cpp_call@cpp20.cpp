struct thingType_ { void Before(auto...) const {} };
const thingType_ thing;
int main() {
thing.Before(1);
    return 0;
}
