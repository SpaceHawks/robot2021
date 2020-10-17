// Uses command line input instead of controller

const ws = require("nodejs-websocket");
const EventEmitter = require("events");
const ioHook = require("iohook");

// make `process.stdin` begin emitting "keypress" events

// let xbox = require('../node-xboxdrv');
// let controller = new xbox('045e', '0719', { type: 'xbox360-wireless', deadzone: 10000 });

let values = { leftX: 0, leftY: 0, rightX: 0, rightY: 0 };

const datalog = new EventEmitter();

ioHook.on("keypress", (event) => {
    if (event?.rawcode) {
        const input = String.fromCharCode(event.rawcode).toLowerCase();
        if (["a", "b", "x", "y"].includes(input)) datalog.emit("data", input);
        else if (input === "l") {
            values.leftX = Math.random() * 2 - 1; // -1, 1
            values.leftY = Math.random() * 2 - 1;
        } else if (input === "r") {
            values.rightX = Math.random() * 2 - 1; // -1, 1
            values.rightY = Math.random() * 2 - 1;
        }
    }
    // {keychar: 'f', keycode: 19, rawcode: 15, type: 'keypress'}
});
ioHook.start();

const ws_server = ws
    .createServer((conn) => {
        console.log("new ws connection");
        datalog.on("data", (data) => conn.sendText(data));
    })
    .listen(8001);

const express = require("express");
const app = express();
const port = process.env.PORT || 3000;

// Set correct headers so control center can make requests
app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header(
        "Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept"
    );
    next();
});

//
app.get("/", (_req, res) => res.send(`Server is running!`));
app.get("/leftX", (_req, res) => res.json(values.leftX));
app.get("/leftY", (_req, res) => res.json(values.leftY));
app.get("/rightX", (_req, res) => res.json(values.rightX));
app.get("/rightY", (_req, res) => res.json(values.rightY));

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
    // askForCommand();
});
