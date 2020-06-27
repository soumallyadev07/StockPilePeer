# Stock Pile Peer

Stock Pile Peer is a simple flask application that uses Machine Learning to predict the stock price of a given company

## Installation & Usage in local Machine

1. Download the repository in your local machine.
2. Check your system for the following libraries:
```python
#Libraries
from flask import Flask,render_template,request
import math
from datetime import date
import datetime
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import re
plt.style.use('fivethirtyeight') 
```
3. After successful installation of all the necessary libraries, open terminal in the app directory and run the following command:
```python
$python3 app.py
```
4. You'll receive a similar output:
```
/usr/local/lib/python3.8/dist-packages/pandas_datareader/compat/__init__.py:7: 
FutureWarning: pandas.util.testing is deprecated. Use the functions in the public API at pandas.testing instead.
  from pandas.util.testing import assert_frame_equal
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
5. Open your preferred browser and past the link [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Cloud Deployment

I've tried to deploy a lite version of this web app on the google cloud platform for a basic overview and technical know-how.

Feel free to check out the following link:
    App Url: [https://bit.ly/StockPilePeer](https://bit.ly/StockPilePeer)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
