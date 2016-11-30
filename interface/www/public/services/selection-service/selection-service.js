app.factory('selectionService', [
    function() {

        // To feed back selection change events to observers.

        var selectionChangeObservers = [];

        // Selection status data model.
        //   start - the first item offset of the selection
        //   end   - the last item offset of the selection
        //   current_offset - while in selection this offset
        //           shows the current location offset

        var status = {
            "primitive": {},
            "start": -1,
            "end": -1,
            "current_offset": -1
        };

        this.resetSelection = function() {
            this.setStartOffset(-1);
            status.end = -1;
            this.setActivePrimitive("", false);
        }

        this.setActivePrimitive = function(value) {
            status.primitive = name;
            this.raiseSelectionChange();
        }

        this.isSelectionActive = function() {
            if (status.current_offset == -1) {
                // no selection active
                return false;
            } else {
                // selection active
                return true;
            }
        }

        this.addSelectionChangeObserver = function(callback) {
            selectionChangeObservers.push(callback);
        }

        this.raiseSelectionChange = function() {
            angular.forEach(selectionChangeObservers, 
                            function(callback){
                callback(status);
            });
        }

        this.updateCurrentOffset = function(value) {
            if (this.isSelectionActive() == true) {
                status.current_offset = value;
                this.raiseSelectionChange();
            }
        }

        this.setStartOffset = function(value) {
            status.start = value;
            status.current_offset = value;
        }

        // Mark the end of the selection and set current_offset
        // to -1 indicating that we are not in selection mode.
        // If the end offset is less than the start offset the
        // user made a selection backwards so we swap start and
        // end offsets.
        this.setEndOffset = function(value) {
            status.end = value;
            var s = status.start;
            var e = status.end;
            if (e < s) {
                status.start = e;
                status.end = s;
            }
            status.current_offset = -1;
        }

        return this;
    }
]);
