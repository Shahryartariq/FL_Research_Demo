import Web3 from 'web3';
import configuration from '../build/contracts/myTime.json';
import 'bootstrap/dist/css/bootstrap.css';

const CONTRACT_ADDRESS = configuration.networks['5777'].address;
const CONTRACT_ABI = configuration.abi;

const web3 = new Web3(Web3.givenProvider || 'http://127.0.0.1:7545');
const contract = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);

let account;

const accountEl = document.getElementById('account');
const durationEl = document.getElementById('duration');
const startTransactionBtn = document.getElementById('startTransaction');

const measureTransactionTime = async () => {
  const startTime = Date.now();

  // A sample function call to the smart contract (e.g., buying a ticket)
  await contract.methods.buyTicket(1).send({ from: account, value: web3.utils.toWei('0.01', 'ether') });

  const endTime = Date.now();
  const duration = (endTime - startTime) / 1000; // Duration in seconds
  durationEl.innerText = `Transaction Duration: ${duration} seconds`;
};

const main = async () => {
  const accounts = await web3.eth.requestAccounts();
  account = accounts[0];
  accountEl.innerText = account;

  startTransactionBtn.onclick = measureTransactionTime;
};

main().catch(console.error);
