from time import sleep
from flask import Flask
from dapr.clients import DaprClient
import os

app = Flask(__name__)
cron_binding_name = 'input-binding'
sql_binding = 'output-binding'
app_port = os.getenv('APP_PORT', '8080')

# Create the table and insert some data
def on_init():
    with DaprClient() as d:
        sqlCmd = "CREATE TABLE orders ( orderId INT, customer TEXT, price FLOAT ); " + \
                "INSERT INTO orders VALUES (1, 'John', 100.0); " + \
                "INSERT INTO orders VALUES (2, 'Jane', 200.0); " + \
                "INSERT INTO orders VALUES (3, 'Jack', 300.0); "

        metadata = {'sql': sqlCmd}

        print(sqlCmd, flush=True)

        try:
            sleep(5)
            d.invoke_binding(binding_name=sql_binding, operation='exec',
                                    binding_metadata=metadata, data='')
        except Exception as e:
            print(e, flush=True)
            raise SystemExit(e)


# Triggered by Dapr input binding
@app.route('/' + cron_binding_name, methods=['POST'])
def show_table_content():
    with DaprClient() as d:
        sql_query = ("SELECT * FROM orders")
        metadata = {'sql': sql_query}

        print(sql_query, flush=True)

        try:
            resp = d.invoke_binding(binding_name=sql_binding, operation='query',
                                    binding_metadata=metadata, data='')
            
            print(resp.json(), flush=True)
            return str(resp.json())

        except Exception as e:
            print(e, flush=True)
            raise SystemExit(e)


on_init()
app.run(port=app_port)
