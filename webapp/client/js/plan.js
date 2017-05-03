import { Template } from 'meteor/templating';
import { plansHandle } from './main';


Template.plan.helpers({
    plansReady() {
        return plansHandle.ready();
    },
    plans() {
        return Plans.find();
    },
});

Template.plan.events({
    'click .btn-save-proposal'(evt) {
        evt.preventDefault();
        const locationName = $("#locationInput").val();
        const currentProposal = Session.get("currentProposal");

        const dateRange = $("#dateTimeInput").data("daterangepicker");
        currentProposal.dateTime = dateRange.startDate.toDate();

        currentProposal.meetingPoint = $("#meetingPointInput").val();
        Meteor.call("saveProposal", currentProposal, locationName, (err)=> {
            if (err) {
                alert(err);
            } else {
                Router.go("/");
            }
        });
        return false;
    },
    'click .btn-cancel'(evt) {
        evt.preventDefault();
        Router.go("/");
        return false;
    },
    'click .location-label'() {
        $("#locationInput").val(this.name);
    }
});

/*
Template.plan.onRendered(function () {
        const dateTimeInput = $("#dateTimeInput");
        dateTimeInput.daterangepicker({
            "singleDatePicker": true,
            "timePicker": true,
            "timePicker24Hour": true,
            "locale": {
                "format": "DD.MM.YYYY HH:mm",
                "separator": " - ",
                "applyLabel": "Ok",
                "cancelLabel": "Abbruch",
                "fromLabel": "Von",
                "toLabel": "Bis",
                "customRangeLabel": "Benutzerdef.",
                "weekLabel": "W",
                "daysOfWeek": [
                    "So",
                    "Mo",
                    "Di",
                    "Mi",
                    "Do",
                    "Fr",
                    "Sa"
                ],
                "monthNames": [
                    "Januar",
                    "Februar",
                    "März",
                    "April",
                    "Mai",
                    "Juni",
                    "Juli",
                    "August",
                    "September",
                    "Oktober",
                    "November",
                    "Dezember"
                ],
                "firstDay": 1
            }

        });

        const dateRange = dateTimeInput.data("daterangepicker");
        if (dateRange) {
            const proposal = Session.get("currentProposal");
            const proposalDateTime = moment(proposal.dateTime);
            dateRange.startDate = proposalDateTime;
            dateRange.endDate = proposalDateTime;
            const format = dateRange.locale.format;
            dateTimeInput.val(proposalDateTime.format(format));
        }

    }
);
*/
