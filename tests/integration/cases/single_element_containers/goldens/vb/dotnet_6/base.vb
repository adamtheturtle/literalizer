Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"single_map", New Object() {New Dictionary(Of String, Object) From {}}},
        {"single_list", New Object() {New Object() {1}}},
        {"single_deep", New Object() {New Object() {New Integer() {2}}}}
    }
End Module
