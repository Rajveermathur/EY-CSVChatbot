# Project Setup
## Paste the csv to be analysed in the main directory of the project
## Make a .env file and paste your groq api key and csv file name as following,
```plaintext
GROQ_API_KEY = <your-groq-api-key>
FILE_NAME = <csv file name>
```
## Run the below command to install all dependencies
```bash
pip install -r requirements.txt
```
## To run the backend app.py, run the below command
```bash
python app.py
```
## To run the fronend, interface.py run the following
```bash
streamlit run interface.py
```