<div layout="row"
     layout-align="center center"
     class="hex-value"
     style="background-color: #{{bgcolor}} !important" 
     ng-class="{selected: selected}"
     ng-mouseover="showProperties()"
     ng-click="byteSelected()">
     {{render}}
</div>
