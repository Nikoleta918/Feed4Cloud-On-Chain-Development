const Web3 = require('web3');
const web3 = new Web3('https://red-b.alastria.io/v0/e4024dc05ccdb514d3b417badf01e078');

//const Web3 = require("web3-eea");
//const web3 = new Web3(new Web3("'http://54.195.253.191:8545'"), 2020);

require('dotenv').config({ path: '../.env' });

const abi = require('../../ABI_alastria.json');
const Feed4CloudSmartContractAddress = process.env.CONTRACT_ADDRESS;
const Feed4CloudSmartContract = new web3.eth.Contract(abi, Feed4CloudSmartContractAddress);

const wallet_address = process.env.WALLET_ADDRESS;

const private_key = process.env.PRIVATE_KEY;

const schedule = require('node-schedule');
const { spawn } = require('child_process');

let rating;
let on = true;
let first_attack = true;


function on_off() {
    let onTime;

    on = !on;   
    
    if (on) {
        onTime = Math.floor(Math.random() * 3 * (10 ** 6)) + (3 * (10 ** 6));
    }
    else {
        if (first_attack) {
            onTime = Math.floor(Math.random() * 3 * (10 ** 6)) + (9 * (10 ** 6));
            first_attack = !first_attack;
        }
        else {
            onTime = Math.floor(Math.random() * 3 * (10 ** 6)) + (21 * (10 ** 6));
        }
    }    
    console.log(`next behavior change in ${onTime/60000} minutes`);
    setTimeout(on_off, onTime);
}


async function submitRating() {
    // spawn new child process to call the python script
    const python = spawn('C:\\Users\\Iwanna\\PycharmProjects\\approx-qoe-distribution\\Feed4Cloud\\Scripts\\python.exe', ['C:\\Users\\Iwanna\\PycharmProjects\\approx-qoe-distribution\\scripts\\evaluation_script.py']);

    // collect data from script
    var expectedQoE = [];
    python.stdout.on('data', async function (data) {
        const output = data.toString();
        console.log(output);

        const qoeValues = output.match(/\d+(\.\d+)?/g).map(Number);
        const weights = [0.25, 0.05, 0.25, 0.1, 0.1, 0.25];

        expectedQoE.push(...qoeValues);

        const weightedSum = qoeValues.reduce((sum, value, index) => sum + value * weights[index], 0);
        const weightSum = weights.reduce((sum, weight) => sum + weight, 0);
        const weightedAverage = weightedSum / weightSum;

        console.log(`Weighted Average QoE: ${weightedAverage}`);

        if (on) {
            console.log('Attack is on!');
            //let fake = Math.random();

            //if (fake <= 0.5) {

            if (weightedAverage >= 3) {
                rating = Math.floor(weightedAverage) - 2;
            } else {
                rating = Math.max(1, Math.floor(weightedAverage) - 1);
            }

            //} else {
            //    rating = Math.round(weightedAverage);
            //}
        } else {
            console.log('Attack is off!');
            rating = Math.round(weightedAverage);
        }

        console.log(`Rating: ${rating}`);

        let tx = await Feed4CloudSmartContract.methods.setRating(74178, rating);
        let encoded_tx = tx.encodeABI();
        let transaction = {
            nonce: await web3.eth.getTransactionCount(wallet_address, 'pending'),
            gasPrice: await web3.eth.getGasPrice(),
            gasLimit: 500000,
            chainId: 2020,
            data: encoded_tx,
            from: wallet_address,
            to: Feed4CloudSmartContractAddress
        };

        
        let signedTx = await web3.eth.accounts.signTransaction(transaction, private_key);
        await web3.eth.sendSignedTransaction(signedTx.rawTransaction);


       
    });

    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
}

function main() {

    on_off();

    // call every 1 minutes
    schedule.scheduleJob('*/1 * * * *', () => {
        submitRating();
    });    
}

main();
