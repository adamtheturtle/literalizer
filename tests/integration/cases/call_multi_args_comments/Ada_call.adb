with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Ts : A_Val; Start : A_Val; End : A_Val) is begin null; end Process;
begin
    Process(ts => AInt (1), start => AInt (0), end => AInt (3600));  -- Jan 1 1970 00:00:00 - 01:00:00
    Process(ts => AInt (5), start => AInt (0), end => AInt (3600));  -- Jan 1 1970 00:00:05 - 01:00:05
    Process(ts => AInt (2), start => AInt (0), end => AInt (5400));  -- Jan 1 1970 00:00:02 - 01:30:02
end Main;
