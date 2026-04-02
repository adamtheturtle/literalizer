Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"my-key", "value1"},
            {"another-key", "value2"},
            {"normal_key", "value3"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"my-key", "value1"},
            {"another-key", "value2"},
            {"normal_key", "value3"}
        }
    End Sub
End Module
