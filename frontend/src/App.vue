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
const ip_port = ref("api.llm-viewer.com:5000");
const availableModelIds = ref([]);

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
      <Graph></Graph>
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
</style>