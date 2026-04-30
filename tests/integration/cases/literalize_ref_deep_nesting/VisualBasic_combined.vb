Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", New Dictionary(Of String, Object) From {{"b", New Dictionary(Of String, Object) From {{"c", New Dictionary(Of String, Object) From {{"$ref", "deep"}}}}}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"a", New Dictionary(Of String, Object) From {{"b", New Dictionary(Of String, Object) From {{"c", New Dictionary(Of String, Object) From {{"$ref", "deep"}}}}}}}
        }
    End Sub
End Module
