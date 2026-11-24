#include <cjson/cJSON.h>
static void consume_widget(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *literalizer_shared_n0 = cJSON_CreateArray();
cJSON *literalizer_shared_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(literalizer_shared_n0, literalizer_shared_n1);
cJSON *literalizer_shared_n2 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(literalizer_shared_n0, literalizer_shared_n2);
cJSON *shared = literalizer_shared_n0;
cJSON *literalizer_my_data_n0 = cJSON_CreateArray();
cJSON *literalizer_my_data_n1 = cJSON_CreateNumber((double)0);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n1);
cJSON *my_data = literalizer_my_data_n0;
consume_widget(my_data);
my_data = shared;
consume_widget(my_data);
    return 0;
}
