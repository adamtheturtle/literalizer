#include <cjson/cJSON.h>
static void consume_widget(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateNumber((double)0);
cJSON_AddItemToObject(literalizer_my_data_n0, "a", literalizer_my_data_n1);
cJSON *my_data = literalizer_my_data_n0;
consume_widget(my_data);
cJSON *literalizer_my_data_m0 = cJSON_CreateObject();
cJSON *literalizer_my_data_m1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(literalizer_my_data_m0, "a", literalizer_my_data_m1);
my_data = literalizer_my_data_m0;
consume_widget(my_data);
    return 0;
}
