'use strict';

const express = require('express');
const Sequelize = require('sequelize')
const sequelize = new Sequelize('postgres://myuser:password@sampleapp.pgo.svc.cluster.local:5432/sampleapp')

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();
app.get('/', (req, res) => {
    sequelize.authenticate().then(() => {
        console.log('Connection has been established successfully.');
        res.status(200).send("Connection to database successful")
    }).catch(err => {
        res.status(404).send("Oh uh, something went wrong");
    });
});

app.get('/health-check',(req,res)=> {
    res.send ("Health check passed");
});

app.get('/bad-health',(req,res)=> {
    res.status(500).send('Health check did not pass');
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);