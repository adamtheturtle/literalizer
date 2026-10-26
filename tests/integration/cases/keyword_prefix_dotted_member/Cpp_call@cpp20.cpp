struct thingType_ { void first_value(auto...) const {} };
const thingType_ thing;
int main() {
thing.first_value(1);
    return 0;
}
