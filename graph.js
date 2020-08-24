
//document.body.innerHTML = "There is some extent";
function myFunction() {

	var subId = document.getElementById("sid").value;
	var day = document.getElementById("day").value;

	const spawn = require("child_process").spawn;

	const process = spawn('python',['./helper.py', subId, day]);

	process.stdout.on('data', data => {
		console.log(data.toString());
	});

	document.getElementById("endgoal").value = "The process is running in the background, Please check the folder with the python program for the Adjacency matrix file "

}
const spawn = require("child_process").spawn;

const process = spawn('python',['./helper.py', subId, day]);
a
process.stdout.on('data', data => {
	console.log(data.toString());
});

/*
const spawn = require('child_process').spawn;

const process = spawn('python',['./hello.py', 'alloju']);

process.stdout.on('data', data => {
	console.log(data.toString());
});


 */
