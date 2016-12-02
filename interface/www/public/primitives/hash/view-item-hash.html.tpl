<div layout="row" layout-wrap
     ng-mouseover="showPrimitiveProperties()"
     ng-click="showModifyPrimitiveProperties()">
    <byte-view ng-repeat="byte in value.properties.value track by $index"
               parent="value"
               type="value.primitive"
               offset="$index"
               value="byte" />
</div>

