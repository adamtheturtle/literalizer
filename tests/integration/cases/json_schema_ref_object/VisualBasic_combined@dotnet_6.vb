Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"schema", New Dictionary(Of String, Object) From {{"$ref", "#/defs/Foo"}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"schema", New Dictionary(Of String, Object) From {{"$ref", "#/defs/Foo"}}}
        }
    End Sub
End Module
