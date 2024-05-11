# LLM-ANALYSIS

<img src="figs/eye.png" alt="LLM-Viewer" width="50"/>


```
# Comparative Analysis of Language Models (LLMs)

This project aims to provide a comprehensive comparative analysis of various Language Models (LLMs) across different hardware configurations. It allows users to evaluate the performance characteristics, computational requirements, and memory usage of LLMs through an interactive web interface.

## Contributors

- Prithvi Chilka
- Nihar Shah
- Dheemanth Reddy

## Features

- Analyze and compare the performance of different LLMs, including models from Hugging Face and custom models hosted on Google Cloud Platform (GCP) Vertex AI.
- Evaluate LLMs on various hardware configurations to understand their computational requirements and performance trade-offs.
- Visualize the model architecture, computational graph, and performance metrics through an intuitive web interface.
- Estimate the inference time, memory consumption, and other key metrics for different LLMs and hardware setups.
- Support for both local deployment and cloud-based deployment on GCP.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Node.js and npm (for the frontend)
- GCP account and project (for deploying custom models on Vertex AI)

### Installation

Clone the repository:
git clone https://github.com/your-username/llm-analysis.git
cd llm-analysis

Install the backend dependencies:
pip install -r requirements.txt

Install the frontend dependencies:
cd frontend
npm install

### Configuration

- Update the backend_settings.py file with your custom model endpoints and project details for GCP Vertex AI.
- Configure the desired hardware settings in the hardware_params.py file.
- Customize the model configurations in the configs directory for each LLM you want to analyze.

### Running the Application

Start the backend server:
python backend_app.py

Start the frontend development server:
cd frontend
npm run serve

Access the web interface by opening a browser and navigating to http://localhost:8080.

## Usage

- Select the desired LLM from the dropdown menu in the web interface.
- Choose the hardware configuration you want to evaluate the LLM on.
- Specify the inference settings, such as batch size, sequence length, and quantization parameters.
- After adding the input text in the inference section Click the "Run Infrence" button to start the networkwise analysis.
- Explore the visualization of the model architecture, computational graph, and performance metrics.
- Customize the analysis by adjusting the inference settings and comparing different LLMs and hardware configurations.

## Deployment

To deploy the application on GCP, follow these steps:

- Set up a GCP project and enable the necessary APIs.
- Deploy your custom models on GCP Vertex AI and obtain the endpoint details.
- Update the backend_settings.py file with the appropriate endpoint information.
- Deploy the backend server on a GCP instance or using a serverless framework like Cloud Functions.
- Build the frontend application for production:
cd frontend
npm run build
- Deploy the frontend static files to a web server or a cloud storage bucket.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

## Acknowledgements

The comparative analysis is based on the research and methodologies proposed in relevant academic papers and industry best practices. We would like to thank the open-source community for providing valuable tools, libraries, and resources that made this project possible.
```