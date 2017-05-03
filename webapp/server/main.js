import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {

    //serverside mqtt in-stream
    Messages.mqttConnect(
        "mqtt://192.168.10.23:1883",
        ["de.scyv/smartswitch/status"],
        {insert: true}
    );});


Meteor.publish("plans", function () {
    return Plans.find();
});


