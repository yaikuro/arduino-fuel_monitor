"""Inventory & Tracking Application."""
import eventlet


from flask import Flask, session
from flask import render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap


eventlet.monkey_patch()

app = Flask('__name__')
app.secret_key = 'beepe.tm'

app.config['MQTT_BROKER_URL'] = '192.168.43.193'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'flask-mqtt'

mqtt = Mqtt(app)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

data = {
    "payload": ""
}

@app.route('/')
def home():
    """Home."""
    return render_template('sensor.html')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    """Connect MQTT Server."""
    mqtt.subscribe('/device/#', 2)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    """Get MQTT message."""
    msg = message.payload.decode()
    data["payload"] = msg
    socketio.emit('sensor', data=data)
    print("Payload: {}".format(data['payload']))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='5000')
