with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AStr ("prefix ${HOME} suffix"),
        AStr ("${interpolated}")
    ];
begin
    my_data := AList'[
        AStr ("prefix ${HOME} suffix"),
        AStr ("${interpolated}")
    ];
end Check;
