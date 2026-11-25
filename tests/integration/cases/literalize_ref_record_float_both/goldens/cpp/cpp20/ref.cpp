int main() {
auto first = 3.5;
auto&& my_data = first;
(void)my_data;
my_data = first;
    (void)my_data;
    return 0;
}
