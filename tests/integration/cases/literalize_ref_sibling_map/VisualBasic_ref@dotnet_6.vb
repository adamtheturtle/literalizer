Imports System.Collections.Generic
Module Check
    Dim SiblingMap = New Dictionary(Of String, Object) From {
        {"k", 2}
    }
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"k", 1}},
        SiblingMap
    }
End Module
