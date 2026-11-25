#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_ref_data_n0 = cJSON_CreateArray();
cJSON *literalizer_ref_data_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(literalizer_ref_data_n0, literalizer_ref_data_n1);
cJSON *literalizer_ref_data_n2 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(literalizer_ref_data_n0, literalizer_ref_data_n2);
cJSON *ref_data = literalizer_ref_data_n0;
cJSON * my_data = ref_data;
    (void)my_data;
    return 0;
}
