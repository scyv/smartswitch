import { Meteor } from 'meteor/meteor'
import { Random } from 'meteor/random'

Meteor.methods({
    'switch'(switchId, status) {
        const msg = {
            "switch": switchId,
            "status": status,
        };
        Messages.insert({topic: "de.scyv/smartswitch/cmd", message: JSON.stringify(msg), broadcast: true});
    }
});