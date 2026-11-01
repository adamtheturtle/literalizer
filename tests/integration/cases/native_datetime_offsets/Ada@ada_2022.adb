with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("stamps", AList'[AStr ("2001-02-03T04:05:06+00:00:01"), AStr ("2001-02-03T04:05:06-00:00:01"), AStr ("2001-02-03T04:05:06+00:00:00.000001"), AStr ("2001-02-03T04:05:06-00:00:00.000001"), AStr ("2001-02-03T04:05:06+05:30:15.000001"), AStr ("2001-02-03T04:05:06-05:30:15.000001")])
    ];
begin
    null;
end Main;
