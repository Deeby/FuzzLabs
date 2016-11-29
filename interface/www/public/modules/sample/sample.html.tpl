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
                <!-- Could not solve it in a better way. So if there is
                     a new primitive to be supported this list may have
                     to be updated too. -->
                <div ng-repeat="primitive in data track by $index" layout="row" layout-wrap>
                    <primitive-binary    ng-if="primitive.primitive == 'binary'"
                                         value="primitive"></primitive-binary>
                    <primitive-block     ng-if="primitive.primitive == 'block'"
                                         value="primitive"></primitive-block>
                    <primitive-numeric   ng-if="primitive.primitive == 'numeric'"
                                         value="primitive"></primitive-numeric>
                    <primitive-static    ng-if="primitive.primitive == 'static'"
                                         value="primitive"></primitive-static>
                    <primitive-string    ng-if="primitive.primitive == 'string'"
                                         value="primitive"></primitive-string>
                    <primitive-delimiter ng-if="primitive.primitive == 'delimiter'"
                                         value="primitive"></primitive-delimiter>
                    <primitive-hash      ng-if="primitive.primitive == 'hash'"
                                         value="primitive"></primitive-hash>
                    <primitive-increment ng-if="primitive.primitive == 'increment'"
                                         value="primitive"></primitive-increment>
                    <primitive-padding   ng-if="primitive.primitive == 'padding'"
                                         value="primitive"></primitive-padding>
                    <primitive-random    ng-if="primitive.primitive == 'random'"
                                         value="primitive"></primitive-random>
                    <primitive-sizer     ng-if="primitive.primitive == 'sizer'"
                                         value="primitive"></primitive-sizer>
                </div>
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
