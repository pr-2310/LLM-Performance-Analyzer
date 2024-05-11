<script setup>
import Graph from "./components/Graph.vue";
import LeftPannel from "./components/LeftPannel.vue";
import Header from "./components/Header.vue";
import { ref, provide, onMounted } from 'vue';
import axios from 'axios';

const model_id = ref("meta-llama/Llama-2-7b-hf");
const hardware = ref("nvidia_A6000");
const global_update_trigger = ref(1);
const total_results = ref({});
const ip_port = ref("endpoint_name=fprojects/{project_id}/locations/{location}/endpoints/{endpoint_id}");
const availableModelIds = ref([]);
const inputData = ref("");
const inferenceOutput = ref(null);
const memoryAnalysisResults = ref(null);

provide("model_id", model_id);
provide("hardware", hardware);
provide("global_update_trigger", global_update_trigger);
provide("total_results", total_results);
provide("ip_port", ip_port);
provide("availableModelIds", availableModelIds);

const global_inference_config = ref({
  "stage": "decode",
  batch_size: 1,
  seq_length: 1024,
  gen_length: 1,
  w_quant: "FP16",
  a_quant: "FP16",
  kv_quant: "FP16",
  use_flashattention: false
});

provide("global_inference_config", global_inference_config);

async function fetchAvailableModels() {
  try {
    const serverUrl = ip_port.value.startsWith("localhost") ? `http://${ip_port.value}` : `https://${ip_port.value}`;
    const response = await axios.get(`${serverUrl}/get_available`);
    availableModelIds.value = response.data.available_model_ids;
  } catch (error) {
    console.error('Error fetching available models:', error);
  }
}

async function runInference() {
  try {
    const serverUrl = ip_port.value.startsWith("localhost") ? `http://${ip_port.value}` : `https://${ip_port.value}`;
    const response = await axios.post(`${serverUrl}/run_inference`, {
      model_id: model_id.value,
      input_data: inputData.value.trim().split('\n')
    });
    inferenceOutput.value = response.data.output;
    memoryAnalysisResults.value = response.data.memory_summary;
  } catch (error) {
    console.error('Error running inference:', error);
  }
}

onMounted(() => {
  fetchAvailableModels();
});
</script>

<template>
  <div class="app_container">
    <header class="upper_header">
      <Header></Header>
    </header>
    <main class="content">
      <LeftPannel></LeftPannel>
      <div class="main-content">
        <Graph></Graph>
        <div class="inference-section">
          <h3>Inference Task</h3>
          <textarea v-model="inputData" placeholder="Enter input data (one per line)"></textarea>
          <button @click="runInference">Run Inference</button>
          <div v-if="inferenceOutput">
            <h4>Inference Output:</h4>
            <pre>{{ inferenceOutput }}</pre>
          </div>
          <div v-if="memoryAnalysisResults">
            <h4>Memory Analysis Results:</h4>
            <pre>{{ memoryAnalysisResults }}</pre>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.app_container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  background-color: #f0f0f0;
}

.upper_header {
  height: 60px;
  background-color: #2c3e50;
  color: #ecf0f1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 2px solid #34495e;
}

.content {
  display: flex;
  flex: 1;
  background-color: #ffffff;
  flex-direction: column;
}

@media (min-width: 768px) {
  .content {
    flex-direction: row;
  }
}

.main-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 20px;
}

.inference-section {
  margin-top: 20px;
}

textarea {
  width: 100%;
  min-height: 100px;
  margin-bottom: 10px;
}

pre {
  white-space: pre-wrap;
}
</style>