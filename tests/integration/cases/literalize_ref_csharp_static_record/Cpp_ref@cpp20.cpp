struct Record0 { int x{}; };
int main() {
auto ref_data = Record0{
    .x = 1,
};
static auto my_data = ref_data;
    (void)my_data;
    return 0;
}
