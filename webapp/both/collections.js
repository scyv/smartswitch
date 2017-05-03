import { Mongo } from 'meteor/mongo';

/**
 * {
 *   _id: string;
 *   switch: string;
 *
 * }
 */
Plans = new Mongo.Collection("plans");


//shared collection
Messages = new Mongo.Collection("messages");
