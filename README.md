# graph-ing-calculator
Learning aid for visualizing graphs and their algorithms

How to use:
1. Clone the repo
2. Create and activate a virtual environment
3. Recursive pip install from requirements.txt

```sh
git clone https://github.com/alexbcreiner0/graph-ing-calculator.git
cd graph-ing-calculator
python3 -m venv dash
source ./dash/bin/activate
pip3 install -r requirements.txt
```

You should now be able to use the app by running the main.py program, e.g.
```sh
python3 main.py
```
and then copying and pasting the local IP address displayed in your terminal. 

If you want a blank graph to start so that you can create your own using the GUI, give the argument blank:
```sh
python3 main.py blank
```
