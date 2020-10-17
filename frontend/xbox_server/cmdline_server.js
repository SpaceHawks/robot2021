// Uses command line input instead of controller

const ws = require("nodejs-websocket");
const EventEmitter = require("events");
const inquirer = require('inquirer');


// let xbox = require('../node-xboxdrv');
// let controller = new xbox('045e', '0719', { type: 'xbox360-wireless', deadzone: 10000 });

let values = { leftX: 0, leftY: 0, rightX: 0, rightY: 0 };

const datalog = new EventEmitter();

async function askForCommand() {
    const {cmd} = await inquirer.prompt([{
        type: "input",
        name: "cmd",
        message: "Please enter a command"
    }]);

    datalog.emit("data", cmd);
    
    askForCommand();
}

const ws_server = ws.createServer(conn => {
	console.log("new ws connection");
	datalog.on('data', data => conn.sendText(data));
}).listen(8001);

const express = require('express');
const app = express();
const port = process.env.PORT || 3000;


// Set correct headers so control center can make requests
app.use(function(req, res, next) {
	res.header("Access-Control-Allow-Origin", "*");
	res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
	next();
});

//
app.get('/', (_req, res) => res.send(`Server is running!`));
app.get('/leftX', (_req, res) => res.json(values.leftX));
app.get('/leftY', (_req, res) => res.json(values.leftY));
app.get('/rightX', (_req, res) => res.json(values.rightX));
app.get('/rightY', (_req, res) => res.json(values.rightY));

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
    askForCommand();
});
