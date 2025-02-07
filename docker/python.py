from flask import Flask, request, jsonify
from google.cloud import run_v2
from google.api_core import retry
from google.api_core.operation import Operation
from google.protobuf.json_format import MessageToDict
import re


def run_cloud_run_job(project_id: str, location: str, job_id: str, env_vars: list) -> Operation:
    overrides_dict = { 'container_overrides': [{ 'env' : env_vars
                                                 }] }
    print(overrides_dict)

    client = run_v2.JobsClient()

    # Construct the fully qualified job name
    job_name = f"projects/{project_id}/locations/{location}/jobs/{job_id}"

    # Create the RunJobRequest
    request = run_v2.RunJobRequest(name=job_name, overrides=overrides_dict)

    # Run the job
    operation = client.run_job(request=request)
    print(operation.metadata)
    return operation


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/runcmd', methods=['POST'])
def run_command():
    data = request.get_json()
    required_fields = ['input_file',  'config_file', 'model_file']

    missing_keys = [key for key in required_fields if key not in data]
    if missing_keys:
        return jsonify({"error": "Missing fields: " + ", ".join(missing_keys)}), 400

    env_vars = [
        {'name': "input_file", 'value': data['input_file']},
        {'name': "config_file" , 'value': data['config_file']},
        {'name': "model_file", 'value': data['model_file'] }
    ]

    project_id = "inference-front-end"  # Replace with your Google Cloud project ID
    location = "us-central1"        # Replace with your Cloud Run region
    job_id = "infer-jobs"          # Replace with your Cloud Run job ID

    operation = run_cloud_run_job(project_id, location, job_id, env_vars)
    print("Job triggered. Operation details:", operation.metadata.name)
    pattern = r".*/(infer-jobs-[a-z0-9]+)$"

    return jsonify({"task_id": re.search(pattern, operation.metadata.name).group(1)}), 202

@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    client = run_v2.ExecutionsClient()
    # Initialize request argument(s)
    request = run_v2.GetExecutionRequest(
        name="projects/inference-front-end/locations/us-central1/jobs/infer-jobs/executions/" +task_id,
    )
    # Make the request
    response = client.get_execution(request=request)

    dict_proto = MessageToDict(response._pb)

    print(dict_proto.get("conditions"))

    desired_event = [
        event for event in dict_proto.get("conditions")
        if event["type"] == "Completed"
    ]

    if desired_event[0].get("state")== 'CONDITION_FAILED':
        response = {
            'state': desired_event[0].get("state"),
            'status': 'FAILED'
        }
        code = 400
    else:
        response = {
            'state': 'PENDING',
            'status': desired_event[0].get("state")  # this is the exception raised
        }
        code = 200
    return jsonify(response), code



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")