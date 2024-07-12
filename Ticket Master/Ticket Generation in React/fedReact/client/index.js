import Web3 from 'web3';
import configuration from '../build/contracts/FedContract.json';
import 'bootstrap/dist/css/bootstrap.css';

const CONTRACT_ADDRESS =
  configuration.networks['5777'].address;
const CONTRACT_ABI = configuration.abi;

const web3 = new Web3(
  Web3.givenProvider || 'http://127.0.0.1:7545'
);
const contract = new web3.eth.Contract(
  CONTRACT_ABI,
  CONTRACT_ADDRESS
);

let account;
const accountEl = document.getElementById('account');

async function displayGlobalVariableValue() {
  try {
      const globalVariableValue = await contract.methods.getGlobalVariable().call();
      document.getElementById("globalValueLabel").innerText = globalVariableValue;
      console.log("Global Variable Value:", globalVariableValue);
  } catch (error) {
      console.error("Error fetching global variable value:", error);
  }
}

async function interactWithSetterFunction(newValue) {
  try {
      const txParameters = {
          from: account,
          gas: 200000,
      };
      const transaction = await contract.methods.setGlobalVariable(newValue).send(txParameters);
      console.log('Transaction Hash:', transaction.transactionHash);
      window.location.reload(); // Reload the page after successful transaction

  } catch (error) {
      console.error('Error interacting with setter function:', error);
  }
}

const main = async () => {
  const accounts = await web3.eth.requestAccounts();
  account = accounts[0];
  accountEl.innerText = "WalletID:  " + account;
  await displayGlobalVariableValue();
};

main();

// Add listener for submitGlobal button click event
const submitGlobalButton = document.getElementById('submitGlobal');
submitGlobalButton.addEventListener('click', async () => {
  const newValue = document.getElementById('globalValueInputField').value;
  await interactWithSetterFunction(newValue);
  await displayGlobalVariableValue();

});
