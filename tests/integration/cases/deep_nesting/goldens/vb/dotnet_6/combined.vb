Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"level1", New Dictionary(Of String, Object) From {{"level2", New Dictionary(Of String, Object) From {{"level3", New Dictionary(Of String, Object) From {{"level4", New Dictionary(Of String, Object) From {{"value", "deep"}, {"items", New String() {"a", "b"}}}}}}, {"sibling", 42}}}, {"tags", New Object() {New Dictionary(Of String, Object) From {{"name", "tag1"}, {"meta", New Dictionary(Of String, Object) From {{"priority", 1}, {"labels", New String() {"x", "y"}}}}}}}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"level1", New Dictionary(Of String, Object) From {{"level2", New Dictionary(Of String, Object) From {{"level3", New Dictionary(Of String, Object) From {{"level4", New Dictionary(Of String, Object) From {{"value", "deep"}, {"items", New String() {"a", "b"}}}}}}, {"sibling", 42}}}, {"tags", New Object() {New Dictionary(Of String, Object) From {{"name", "tag1"}, {"meta", New Dictionary(Of String, Object) From {{"priority", 1}, {"labels", New String() {"x", "y"}}}}}}}}}
        }
    End Sub
End Module
