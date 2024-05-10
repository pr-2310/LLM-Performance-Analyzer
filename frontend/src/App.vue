<script setup>
// import { defineAsyncComponent } from 'vue'

// const Graph = defineAsyncComponent(() =>
//   import('./components/Graph.vue')
// )

import Graph from "./components/Graph.vue"
import LeftPannel from "./components/LeftPannel.vue"
import Header from "./components/Header.vue"
import { ref, computed, provide } from 'vue';

const model_id = ref("meta-llama/Llama-2-7b-hf");
const hardware = ref("nvidia_A6000");
const global_update_trigger = ref(1);
const total_results = ref({});
const ip_port = ref("api.llm-viewer.com:5000");

provide("model_id", model_id);
provide("hardware", hardware);
provide("global_update_trigger", global_update_trigger);
provide("total_results", total_results);
provide("ip_port", ip_port);


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

</script>

<template>
  <div class="app_container">
    <div class="upper_header">
      <Header></Header>
    </div>
    <div class="bottom-block">
      <LeftPannel></LeftPannel>
      <Graph></Graph>
    </div>

  </div>
</template>

<style>
body {
  overflow-x: hidden;
  overflow-y: hidden;
}

.app_container {
  /* display: flex;
  flex-direction: column;
  width: 98vw; */
  width: 100%;
  height: 100vh;

}

.upper_header {
  flex: 1;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 50px;
  border-bottom: 1px solid #333333;
  background-color: #D6DBDF;
}

.bottom-block {
  display: flex;
  flex-direction: row;
  height: calc(100% - 60px);
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
