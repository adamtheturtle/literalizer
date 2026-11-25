with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("below", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AInt (1)]]]]]]]]),
        AEntry ("boundary", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AInt (2)]]]]]]]]]),
        AEntry ("multiple", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AInt (3)]]]]]]]]]]]]]]]]]),
        AEntry ("text", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AStr ("value")]]]]]]]]]),
        AEntry ("boolean", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[ABool (True)]]]]]]]]]),
        AEntry ("float", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AFloat (1.5)]]]]]]]]])
    ];
begin
    my_data := AMap'[
        AEntry ("below", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AInt (1)]]]]]]]]),
        AEntry ("boundary", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AInt (2)]]]]]]]]]),
        AEntry ("multiple", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AInt (3)]]]]]]]]]]]]]]]]]),
        AEntry ("text", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AStr ("value")]]]]]]]]]),
        AEntry ("boolean", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[ABool (True)]]]]]]]]]),
        AEntry ("float", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AFloat (1.5)]]]]]]]]])
    ];
end Main;
