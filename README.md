# InteractiveBrokerAPI

Working Script to fetch the data from the Interactive Brokers via TWS API by IB.


### Instructions to setup

1. Install TWS from https://www.interactivebrokers.co.in/en/index.php?f=16040 

2. Follow https://interactivebrokers.github.io/tws-api/initial_setup.html to activate API access. enter the port as 7497

3. Install IB API folder from http://interactivebrokers.github.io/

4. unzip the folder and run the following on terminal. This is to install the ibapi package in python.

```
cd IBJts/source/pythonclient
python3 setup.py install
```

5. navigate to working directory and run
```
git clone https://gitea.geminisolutions.in/ha.jain/InteractiveBrokerAPI.git
cd InteractiveBrokerAPI
python3 main.py
```
