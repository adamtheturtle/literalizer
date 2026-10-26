auto process(auto...) { return 0; }
int main() {
static_cast<void>(process(1));
static_cast<void>(process(2));
    return 0;
}
