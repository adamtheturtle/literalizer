Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            True,
            1.5,
            Nothing,
            "2020-01-01",
            "2020-01-01T00:00:00+00:00",
            New Object() {}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            True,
            1.5,
            Nothing,
            "2020-01-01",
            "2020-01-01T00:00:00+00:00",
            New Object() {}
        }
    End Sub
End Module
