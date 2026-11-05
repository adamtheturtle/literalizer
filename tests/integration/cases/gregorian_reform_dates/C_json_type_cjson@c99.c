#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("1500-03-01");
cJSON_AddItemToObject(literalizer_my_data_n0, "ancient_date", literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateString("2024-01-15");
cJSON_AddItemToObject(literalizer_my_data_n0, "modern_date", literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateString("1582-10-04");
cJSON_AddItemToObject(literalizer_my_data_n0, "before_date", literalizer_my_data_n3);
cJSON *literalizer_my_data_n4 = cJSON_CreateString("1582-10-10");
cJSON_AddItemToObject(literalizer_my_data_n0, "gap_date", literalizer_my_data_n4);
cJSON *literalizer_my_data_n5 = cJSON_CreateString("1582-10-15");
cJSON_AddItemToObject(literalizer_my_data_n0, "transition_date", literalizer_my_data_n5);
cJSON *literalizer_my_data_n6 = cJSON_CreateString("1582-10-16");
cJSON_AddItemToObject(literalizer_my_data_n0, "after_date", literalizer_my_data_n6);
cJSON *literalizer_my_data_n7 = cJSON_CreateString("1582-10-04T12:30:00.000001Z");
cJSON_AddItemToObject(literalizer_my_data_n0, "before_naive", literalizer_my_data_n7);
cJSON *literalizer_my_data_n8 = cJSON_CreateString("1582-10-10T12:30:00.500000Z");
cJSON_AddItemToObject(literalizer_my_data_n0, "gap_naive", literalizer_my_data_n8);
cJSON *literalizer_my_data_n9 = cJSON_CreateString("1582-10-15T00:30:00+18:00");
cJSON_AddItemToObject(literalizer_my_data_n0, "transition_positive", literalizer_my_data_n9);
cJSON *literalizer_my_data_n10 = cJSON_CreateString("1582-10-15T23:30:00-18:00");
cJSON_AddItemToObject(literalizer_my_data_n0, "transition_negative", literalizer_my_data_n10);
cJSON *literalizer_my_data_n11 = cJSON_CreateString("1582-10-16T00:30:00+18:00");
cJSON_AddItemToObject(literalizer_my_data_n0, "after_positive", literalizer_my_data_n11);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
