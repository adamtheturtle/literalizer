-module(fixture_gregorian_reform_dates_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"ancient_date"/utf8>> => <<"1500-03-01"/utf8>>,
        <<"modern_date"/utf8>> => <<"2024-01-15"/utf8>>,
        <<"before_date"/utf8>> => <<"1582-10-04"/utf8>>,
        <<"gap_date"/utf8>> => <<"1582-10-10"/utf8>>,
        <<"transition_date"/utf8>> => <<"1582-10-15"/utf8>>,
        <<"after_date"/utf8>> => <<"1582-10-16"/utf8>>,
        <<"before_naive"/utf8>> => <<"1582-10-04T12:30:00.000001"/utf8>>,
        <<"gap_naive"/utf8>> => <<"1582-10-10T12:30:00.500000"/utf8>>,
        <<"transition_positive"/utf8>> => <<"1582-10-15T00:30:00+18:00"/utf8>>,
        <<"transition_negative"/utf8>> => <<"1582-10-15T23:30:00-18:00"/utf8>>,
        <<"after_positive"/utf8>> => <<"1582-10-16T00:30:00+18:00"/utf8>>
    },
    My_data.
