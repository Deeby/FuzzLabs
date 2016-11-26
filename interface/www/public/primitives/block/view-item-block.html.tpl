<div layout="row" layout-wrap>
    <byte-view ng-repeat="byte in value.properties.value track by $index" offset="$index" value="byte" />
</div>

