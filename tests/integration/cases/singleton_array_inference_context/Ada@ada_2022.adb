with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("nil", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[ANull]]]]]]]]]),
        AEntry ("empty", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[]]]]]]]]]]),
        AEntry ("siblings", AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AList'[AInt (4), AInt (5)]]]]]]]]]])
    ];
begin
    null;
end Main;
