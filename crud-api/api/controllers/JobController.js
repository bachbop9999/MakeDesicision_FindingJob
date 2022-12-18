'use strict'

const util = require('util')
const mysql = require('mysql')
const db = require('./../db')

module.exports = {
    getField: (req, res) => {
        let sql = 'SELECT * FROM field'
        db.query(sql, (err, response) => {
            if (err) throw err
            res.json(response)
        })
    },

    getDegree: (req, res) => {
        let sql = 'SELECT * FROM degree'
        db.query(sql, (err, response) => {
            if (err) throw err
            res.json(response)
        })
    },

    getProvince: (req, res) => {
        let sql = 'SELECT * FROM province'
        db.query(sql, (err, response) => {
            if (err) throw err
            res.json(response)
        })
    },

    districtByProvince: (req, res) => {
        let provinceId = req.query.provinceId;
        let sql = 'SELECT * FROM district where provinceId = ?'
        db.query(sql, [provinceId], (err, response) => {
            if (err) throw err
            res.json(response)
        })
    },

    getJobById: (req, res) => {
        let jobId = req.query.jobId;
        let sql = 'SELECT id, companyName FROM jobv2 where id = ?'
        db.query(sql, [jobId], (err, response) => {
            if (err) throw err
            res.json(response)
        })
    },

    getAllJob: (req, res) => {
        let jobId = req.query.jobId;
        let sql = 'SELECT a.id, a.`expYear`, a.`companyName` AS companyName, a.`minSalary`, a.`maxSalary`, b.`name` AS degreeName, c.`fieldName`, d.`name` AS districtName, e.`_name` AS provinceName FROM jobv2 a JOIN degree b ON a.`degreeId` = b.`id` JOIN `field` c ON a.`fieldId` = c.`id` JOIN district d ON a.`districtId` = d.`id` JOIN province e ON a.`provinceId` = e.`id`'
        db.query(sql, [jobId], (err, response) => {
            if (err) throw err
            res.json(response)
        })
    }
}