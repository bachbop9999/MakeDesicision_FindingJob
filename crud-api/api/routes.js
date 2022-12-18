'use strict';
module.exports = function (app) {
  let jobCtrl = require('./controllers/JobController');

  // todoList Routes
  app.route('/fields')
    .get(jobCtrl.getField);

  app.route('/degrees')
    .get(jobCtrl.getDegree);

  app.route('/provinces')
    .get(jobCtrl.getProvince);

  app.route('/districtByProvince')
    .get(jobCtrl.districtByProvince);

  app.route('/getJobById')
    .get(jobCtrl.getJobById);

  app.route('/getAllJob')
    .get(jobCtrl.getAllJob);

};