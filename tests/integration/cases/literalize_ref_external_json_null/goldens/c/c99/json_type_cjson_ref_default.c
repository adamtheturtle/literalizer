#include <cjson/cJSON.h>
static void consume_widget(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *literalizer_item_n0 = cJSON_CreateNull();
cJSON *item = literalizer_item_n0;
cJSON *literalizer_my_data_n0 = cJSON_CreateNull();
cJSON *my_data = literalizer_my_data_n0;
consume_widget(my_data);
my_data = item;
consume_widget(my_data);
    return 0;
}
