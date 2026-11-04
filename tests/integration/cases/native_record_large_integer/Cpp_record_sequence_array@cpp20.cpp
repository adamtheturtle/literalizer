struct Record0 { long long value{}; };
int main() {
auto my_data = Record0{
    .value = 2147483648,
};
    (void)my_data;
    return 0;
}
