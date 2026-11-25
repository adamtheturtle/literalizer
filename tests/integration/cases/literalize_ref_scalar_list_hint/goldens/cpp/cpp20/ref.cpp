int main() {
auto ref_data = 1;
auto&& my_data = ref_data;
    (void)my_data;
    return 0;
}
