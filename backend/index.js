import express from 'express';
// import "router";
// import Router from "router";
// router = Router();
const app = express();

app.get("/", (req, res)=> {
    res.send("initializing");
});

app.listen(9000, () => {
    console.log("running")
})