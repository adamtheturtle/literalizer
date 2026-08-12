with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AStr ("This long string keeps its structural comma beyond the Fortran wrapping window without a safe split."),
        AInt (1)
    ];
begin
    null;
end Main;
