import { Template } from 'meteor/templating';

import './../view/main.html';

export let plansHandle;

UI.registerHelper("formattedDate", (date) => {
    if (!date) {
        return "-";
    }
    return moment(date).format("DD.MM.YYYY");
});

UI.registerHelper("formattedDateTime", (date) => {
    if (!date) {
        return "-";
    }
    return moment(date).format("DD.MM.YYYY HH:mm");
});

Template.main.helpers({});

Template.main.events({
    'click button'(evt) {
        const switchId = $(evt.target).data("switch");
        const status = $(evt.target).data("status");
        Meteor.call("switch", switchId, status);
    }
});

Meteor.startup(() => {
    moment.locale('de');

    Tracker.autorun(() => {
        plansHandle = Meteor.subscribe("plans");
    });
});
