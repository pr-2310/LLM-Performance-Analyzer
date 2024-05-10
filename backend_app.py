from flask import Flask, request, jsonify
from flask_cors import CORS
from get_model_graph import get_model_graph
from backend_settings import available_hardwares, available_model_ids_sources
import argparse
import torch
from torchsummary import summary
from google.cloud import aiplatform

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def load_model(model_id):
    endpoint = aiplatform.Endpoint(model_id)
    model = endpoint.load_model()
    return model

@app.route("/")
def index():
    return "backend server ready."

@app.route("/get_graph", methods=["POST"])
def get_graph():
    model_id = request.json["model_id"]
    hardware = request.json["hardware"]
    inference_config = request.json["inference_config"]

    nodes, edges, total_results, hardware_info = get_model_graph(
        model_id, hardware, None, inference_config
    )

    return {
        "nodes": nodes,
        "edges": edges,
        "total_results": total_results,
        "hardware_info": hardware_info,
    }

@app.route("/get_available", methods=["GET"])
def get_available():
    if request.host == "localhost:5000":
        custom_model_ids = [model_id for model_id in available_model_ids_sources if model_id.startswith("custom:")]
        return jsonify({
            "available_hardwares": available_hardwares,
            "available_model_ids": custom_model_ids,
        })
    else:
        regular_model_ids = [model_id for model_id in available_model_ids_sources if not model_id.startswith("custom:")]
        return jsonify({
            "available_hardwares": available_hardwares,
            "available_model_ids": regular_model_ids,
        })

@app.route("/run_inference", methods=["POST"])
def run_inference():
    model_id = request.json["model_id"]
    input_data = request.json["input_data"]

    # Load the hosted model from Vertex AI
    model = load_model(model_id)

    # Prepare the input data
    input_tensor = torch.tensor(input_data)

    # Run the inference task
    with torch.no_grad():
        output = model(input_tensor)

    # Perform memory analysis using PyTorch summary
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    memory_summary = summary(model, input_size=input_tensor.shape, device=str(device))

    return jsonify({
        "output": output.tolist(),
        "memory_summary": str(memory_summary),
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    host = "127.0.0.1" if args.local else "0.0.0.0"
    app.run(debug=args.debug, host=host, port=args.port)