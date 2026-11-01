Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"stamps", New String() {"2001-02-03T04:05:06+00:00:01", "2001-02-03T04:05:06-00:00:01", "2001-02-03T04:05:06+00:00:00.000001", "2001-02-03T04:05:06-00:00:00.000001", "2001-02-03T04:05:06+05:30:15.000001", "2001-02-03T04:05:06-05:30:15.000001"}}
    }
End Module
