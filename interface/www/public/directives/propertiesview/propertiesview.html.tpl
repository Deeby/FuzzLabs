<md-tabs md-dynamic-height md-border-bottom>
    <md-tab label="unit">
        <md-content class="md-padding">
            <div layout="column">
                <md-input-container class="md-block" flex-gt-sm>
                    <label>Unit name</label>
                    <input ng-model="unit.name">
                </md-input-container>
                <md-input-container class="md-block">
                    <label>Description</label>
                    <textarea ng-model="unit.description" rows="5" md-maxlength="500">
                    </textarea>
                </md-input-container>
            </div>
        </md-content>
    </md-tab>
    <md-tab label="selection">
        <md-content class="md-padding">
            <div layout="column">
                <table>
                    <tr>
                        <td>Type:</td><td>{{item_type}}</td>
                    </tr>
                    <tr>
                        <td>Offset:</td><td>{{item_offset}} ({{item_offset_hex}})</td>
                    </tr>
                    <tr>
                        <td>Value</td><td>
                            Decimal: {{item_value}}<br>
                            Hex: {{item_value_hex}}<br>
                            Ascii: {{item_value_ascii}}
                        </td>
                    </tr>
                </table>
            </div>
        </md-content>
    </md-tab>
</md-tabs>
