int main() {
auto first = true;
auto&& my_data = first;
(void)my_data;
my_data = first;
    (void)my_data;
    return 0;
}
