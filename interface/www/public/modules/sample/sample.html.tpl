<div id="m-designer" layout-fill>
    <md-toolbar layout-align="center start" md-whiteframe="4">
        <div layout="row" layout-align="start center" layout-padding>
            <img src="/dist/images/logo.svg" width="50" height="50"/>
            <span class="title">Designer</span>
        </div>
    </md-toolbar>

    <div>
        <md-menu-bar>
            <md-menu>
                <button ng-click="$mdOpenMenu()">
                    <md-icon md-font-icon="subject" style="color: #eeeeee">subject</md-icon>
                    Unit
                </button>
                <md-menu-content>
                    <md-menu-item>
                        <md-button ng-click="close()">
                            Close
                        </md-button>
                    </md-menu-item>
                    <md-menu-divider></md-menu-divider>
                    <md-menu-item>
                        <md-button>
                            Exit
                        </md-button>
                    </md-menu-item>
                </md-menu-content>
            </md-menu>
        </md-menu-bar>
    </div>

    <section layout="row" class="work-area">

        <md-sidenav 
            class="md-sidenav-left"
            md-component-id="left"
            md-is-locked-open="true"
            md-whiteframe="4">
            <md-toolbar>
                <h1 class="md-toolbar-tools">Primitives</h1>
            </md-toolbar>
            <md-content layout="column">
                <button-block></button-block>
                <button-numeric></button-numeric>
                <button-static></button-static>
                <button-string></button-string>
                <button-delimiter></button-delimiter>
                <button-binary></button-binary>
                <button-hash></button-hash>
                <button-increment></button-increment>
                <button-padding></button-padding>
                <button-random></button-random>
                <button-sizer></button-sizer>
            </md-content>
        </md-sidenav>

        <md-content flex layout-padding ngf-drop="fileOpen($files)" ondragover="allowDrop(event)">
            <md-card ng-if="opened == true" md-whiteframe="4" layout="row" layout-wrap>
                <!-- TODO: HERE TO RENDER -->
                <byte-view ng-repeat="byte in data track by $index" offset="$index" value="byte" />
                <!-- TODO: HERE TO RENDER -->
            </md-card>
            <div ng-if="opened == false" layout="column" layout-align="center center" layout-fill class="drop-area">
                 <i class="material-icons" style="font-size: 150px; color: #AAAAAA;">cloud_upload</i>
                 <div style="color: #AAAAAA;">Drag and drop a file to this area to open it.</div>
            </div>

        </md-content>

        <md-sidenav class="md-sidenav-right"
                    md-component-id="right"
                    md-is-locked-open="true"
                    md-whiteframe="4">
            <md-toolbar>
                <h1 class="md-toolbar-tools">Properties</h1>
            </md-toolbar>
            <md-content>
                <!-- Content -->
                <properties-view/>
            </md-content>
        </md-sidenav>
    </section>
</div>
