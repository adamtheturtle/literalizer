Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"deep", New Integer()()()() {New Integer()()() {New Integer()() {New Integer() {1}}}}}
    }
End Module
