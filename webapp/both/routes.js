Router.configure({
    layoutTemplate: "layout"
});

Router.route("/", function () {
    this.render("main");
}, {name: "main"});

Router.route('/plan', function () {
    this.render("plan");
}, {name: "plan"});
