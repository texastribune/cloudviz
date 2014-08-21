import json
import os

from flask import Flask, request, jsonify
from whitenoise import WhiteNoise

from cloudviz import get_cloudwatch_data
from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

app = Flask(__name__)


def get_instances():
    """List running instances in a format convenient for us."""
    from boto import ec2
    conn = ec2.connect_to_region('us-east-1')
    # WISHLIST make this more flexible
    instances = conn.get_only_instances(filters={'tag:environment': 'prod'})
    return [{
        'id': x.id,
        'name': x.tags.get('Name'),
        'site': x.tags.get('site'),
        'launch_time': x.launch_time,
    } for x in instances]


def get_elbs():
    """List elastic load balancers."""
    import boto.ec2.elb
    conn = boto.ec2.elb.connect_to_region('us-east-1')
    return [{
        'name': x.name,
        'instance_count': len(x.instances),
        'created_time': x.created_time,
    } for x in conn.get_all_load_balancers()]


# TODO standardize what url to look for
@app.route('/data')
@app.route('/cloudviz')
def main():
    # Parse the query string
    cloudviz_query = json.loads(request.args.get('qs'))

    # Convert tqx to dict; tqx is a set of colon-delimited key/value pairs separated by semicolons
    tqx = {}
    for s in request.args.get('tqx').split(';'):
        key, value = s.split(':')
        tqx.update({key: value})

    # Set reqId so we know who to send data back to
    request_id = tqx['reqId']

    results = get_cloudwatch_data(
        cloudviz_query, request_id, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    return results  # TODO mimetype='text/plain' or javascript


@app.route('/list/ec2')
def list_ec2():
    data = {
        'instances': get_instances(),
    }
    return jsonify(**data)


@app.route('/list/elb')
def list_elb():
    data = {
        'instances': get_elbs(),
    }
    return jsonify(**data)


BASE_DIR = os.path.dirname(__file__)
application = WhiteNoise(app.wsgi_app, max_age=0)
application.add_files(
    os.path.join(BASE_DIR, 'reports'), 'reports', )
app.wsgi_app = application


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
