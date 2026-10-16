Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' outer heading
        ' first empty
        ' second empty
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", New Dictionary(Of String, Object) From {}},
            {"b", New Dictionary(Of String, Object) From {}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' outer heading
        ' first empty
        ' second empty
        my_data = New Dictionary(Of String, Object) From {
            {"a", New Dictionary(Of String, Object) From {}},
            {"b", New Dictionary(Of String, Object) From {}}
        }
    End Sub
End Module
